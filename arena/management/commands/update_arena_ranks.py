from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from arena.models import ArenaRank
from problems.models import UserAttempt


class Command(BaseCommand):
    help = 'Обновляет рейтинги арены на основе активности пользователей за неделю'
    
    def handle(self, *args, **options):
        self.stdout.write('Начало обновления рейтингов арены...')
        
        # Получаем дату неделю назад
        week_ago = timezone.now() - timedelta(days=7)
        
        # Получаем всех активных пользователей
        users = User.objects.filter(is_active=True)
        
        updated_count = 0
        created_count = 0
        
        for user in users:
            # Получаем или создаем запись в арене
            arena_rank, created = ArenaRank.objects.get_or_create(
                user=user,
                defaults={
                    'current_index': user.profile.al_khwarizmi_index,
                    'current_division': ArenaRank.get_division_from_index(
                        user.profile.al_khwarizmi_index
                    )
                }
            )
            
            if created:
                created_count += 1
            
            # Обновляем индекс и дивизион
            arena_rank.current_index = user.profile.al_khwarizmi_index
            arena_rank.current_division = ArenaRank.get_division_from_index(
                arena_rank.current_index
            )
            
            # Подсчитываем очки за неделю
            weekly_attempts = UserAttempt.objects.filter(
                user=user,
                attempt_date__gte=week_ago,
                is_correct=True
            )
            
            arena_rank.weekly_score = sum(
                attempt.points_awarded for attempt in weekly_attempts
            )
            
            arena_rank.save()
            updated_count += 1
        
        # Обновляем ранги внутри каждого дивизиона
        for division in ['NOVICE', 'EUCLID', 'EINSTEIN']:
            ranks = ArenaRank.objects.filter(
                current_division=division
            ).order_by('-weekly_score', '-current_index')
            
            for index, rank in enumerate(ranks, start=1):
                rank.rank = index
                rank.save(update_fields=['rank'])
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Обновление завершено! '
                f'Создано: {created_count}, Обновлено: {updated_count}'
            )
        )
