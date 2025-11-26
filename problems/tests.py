from django.test import TestCase
from django.contrib.auth.models import User
from .models import Topic, Problem, UserAttempt


class ProblemModelTest(TestCase):
    """Тесты для моделей задач"""
    
    def setUp(self):
        """Создаем тестовые данные"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.topic = Topic.objects.create(
            name='Тестовая тема',
            description='Описание темы',
            difficulty_base=1000
        )
        
        self.problem = Problem.objects.create(
            topic=self.topic,
            title='Тестовая задача',
            latex_formula=r'x^2 = 4',
            description='Решите уравнение',
            correct_answer='2',
            difficulty_score=1000,
            solution_steps=['Шаг 1', 'Шаг 2'],
            hints=['Подсказка 1'],
            is_active=True
        )
    
    def test_topic_creation(self):
        """Тест создания темы"""
        self.assertEqual(self.topic.name, 'Тестовая тема')
        self.assertEqual(self.topic.difficulty_base, 1000)
    
    def test_problem_creation(self):
        """Тест создания задачи"""
        self.assertEqual(self.problem.title, 'Тестовая задача')
        self.assertEqual(self.problem.correct_answer, '2')
        self.assertTrue(self.problem.is_active)
    
    def test_user_attempt_creation(self):
        """Тест создания попытки решения"""
        attempt = UserAttempt.objects.create(
            user=self.user,
            problem=self.problem,
            submitted_answer='2',
            is_correct=True,
            points_awarded=150
        )
        
        self.assertEqual(attempt.user, self.user)
        self.assertEqual(attempt.problem, self.problem)
        self.assertTrue(attempt.is_correct)
        self.assertEqual(attempt.points_awarded, 150)
