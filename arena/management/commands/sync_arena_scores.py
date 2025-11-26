"""
Management command для синхронизации очков в арене.
Подсчитывает weekly_score на основе решенных задач.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from arena.models import ArenaRank
from problems.models import UserAttempt
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Синхронизирует очки в арене на основе решенных задач за текущую неделю'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all-time',
            action='store_true',
            help='Подсчитать очки за всё время (не только за неделю)',
        )

    def handle(self, *args, **options):
        all_time = options['all_time']
        
        if all_time:
            self.stdout.write(self.style.WARNING('Подсчет очков за всё время...'))
            time_filter = {}
        else:
            one_week_ago = datetime.now() - timedelta(days=7)
            self.stdout.write(self.style.WARNING(f'Подсчет очков за последнюю неделю (с {one_week_ago})...'))
            time_filter = {'created_at__gte': one_week_ago}
        
        users = User.objects.all()
        updated_count = 0
        skipped_count = 0
        
        for user in users:
            # Проверяем наличие профиля
            if not hasattr(user, 'profile'):
                self.stdout.write(
                    self.style.WARNING(f'⚠️  {user.username}: профиль не найден, пропускаем')
                )
                skipped_count += 1
                continue
            
            # Подсчитываем очки за правильные ответы
            correct_attempts = UserAttempt.objects.filter(
                user=user,
                is_correct=True,
                **time_filter
            )
            
            total_points = sum(attempt.points_awarded or 0 for attempt in correct_attempts)
            
            # Обновляем или создаем запись в арене
            arena_rank, created = ArenaRank.objects.get_or_create(
                user=user,
                defaults={
                    'current_index': user.profile.al_khwarizmi_index,
                    'current_division': ArenaRank.get_division_from_index(
                        user.profile.al_khwarizmi_index
                    ),
                    'weekly_score': total_points
                }
            )
            
            if not created and total_points > 0:
                arena_rank.weekly_score = total_points
                arena_rank.current_index = user.profile.al_khwarizmi_index
                arena_rank.current_division = ArenaRank.get_division_from_index(
                    user.profile.al_khwarizmi_index
                )
                arena_rank.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ {user.username}: {total_points} очков, '
                        f'{correct_attempts.count()} правильных ответов'
                    )
                )
        
        # Обновляем места в рейтинге для всех
        self.stdout.write(self.style.WARNING('Обновление мест в рейтинге...'))
        for arena_rank in ArenaRank.objects.all():
            arena_rank.update_rank()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Готово! Обновлено записей: {updated_count}, '
                f'пропущено пользователей без профиля: {skipped_count}'
            )
        )
