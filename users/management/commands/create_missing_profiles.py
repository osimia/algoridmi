"""
Management command для создания профилей пользователям, у которых их нет.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile


class Command(BaseCommand):
    help = 'Создает профили для пользователей, у которых их нет'

    def handle(self, *args, **options):
        users_without_profile = []
        
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                users_without_profile.append(user)
        
        if not users_without_profile:
            self.stdout.write(
                self.style.SUCCESS('✅ Все пользователи уже имеют профили!')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(
                f'Найдено пользователей без профиля: {len(users_without_profile)}'
            )
        )
        
        created_count = 0
        for user in users_without_profile:
            profile = Profile.objects.create(
                user=user,
                user_type='student',
                age=18,
                country='KZ'
            )
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Создан профиль для: {user.username} (email: {user.email})'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Готово! Создано профилей: {created_count}'
            )
        )
