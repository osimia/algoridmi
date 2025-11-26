from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class ProfileModelTest(TestCase):
    """Тесты для модели Profile"""
    
    def setUp(self):
        """Создаем тестового пользователя"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_creation(self):
        """Тест автоматического создания профиля"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.al_khwarizmi_index, 1000)
    
    def test_division_property(self):
        """Тест определения дивизиона"""
        profile = self.user.profile
        
        profile.al_khwarizmi_index = 400
        self.assertEqual(profile.division, 'Лига Новичков')
        
        profile.al_khwarizmi_index = 1200
        self.assertEqual(profile.division, 'Лига Евклида')
        
        profile.al_khwarizmi_index = 1600
        self.assertEqual(profile.division, 'Лига Эйнштейна')
    
    def test_rank_title_property(self):
        """Тест определения звания"""
        profile = self.user.profile
        
        profile.al_khwarizmi_index = 400
        self.assertEqual(profile.rank_title, 'Новичок')
        
        profile.al_khwarizmi_index = 1200
        self.assertEqual(profile.rank_title, 'Адепт')
        
        profile.al_khwarizmi_index = 2500
        self.assertEqual(profile.rank_title, 'Гроссмейстер')
    
    def test_update_index(self):
        """Тест обновления индекса"""
        profile = self.user.profile
        initial_index = profile.al_khwarizmi_index
        
        # Правильное решение задачи
        delta = profile.update_index(1200, True)
        self.assertGreater(profile.al_khwarizmi_index, initial_index)
        self.assertEqual(profile.total_solved_problems, 1)
        
        # Неправильное решение
        current_index = profile.al_khwarizmi_index
        delta = profile.update_index(1200, False)
        self.assertLess(profile.al_khwarizmi_index, current_index)
