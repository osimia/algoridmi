"""
Management command для массовой генерации задач через Gemini API
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from problems.models import Problem
from core.gemini_service import get_gemini_service
from core.math_topics_database import MATH_TOPICS_DATABASE
import time
import random


class Command(BaseCommand):
    help = 'Массовая генерация задач через Gemini API'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Количество задач для генерации (по умолчанию: 10)'
        )
        parser.add_argument(
            '--grade',
            type=int,
            help='Класс (1-12). Если не указан, генерирует для всех классов'
        )
        parser.add_argument(
            '--difficulty-min',
            type=int,
            default=0,
            help='Минимальная сложность (по умолчанию: 0)'
        )
        parser.add_argument(
            '--difficulty-max',
            type=int,
            default=3000,
            help='Максимальная сложность (по умолчанию: 3000)'
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=2.0,
            help='Задержка между запросами в секундах (по умолчанию: 2.0)'
        )
    
    def handle(self, *args, **options):
        count = options['count']
        grade = options['grade']
        min_diff = options['difficulty_min']
        max_diff = options['difficulty_max']
        delay = options['delay']
        
        self.stdout.write(self.style.SUCCESS(f'\n🚀 Начало массовой генерации задач'))
        self.stdout.write(f'📊 Параметры:')
        self.stdout.write(f'   - Количество: {count}')
        self.stdout.write(f'   - Класс: {grade if grade else "Все классы"}')
        self.stdout.write(f'   - Сложность: {min_diff} - {max_diff}')
        self.stdout.write(f'   - Задержка: {delay} сек\n')
        
        # Получаем сервис Gemini
        try:
            gemini = get_gemini_service()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка инициализации Gemini: {e}'))
            return
        
        # Счетчики
        success_count = 0
        error_count = 0
        
        # Генерируем задачи
        for i in range(count):
            self.stdout.write(f'\n📝 Генерация задачи {i+1}/{count}...')
            
            try:
                # Определяем параметры задачи
                if grade:
                    target_grade = grade
                else:
                    target_grade = random.randint(1, 12)
                
                target_difficulty = random.randint(min_diff, max_diff)
                
                # Выбираем случайную тему из базы данных
                suitable_topics = [
                    topic for topic in MATH_TOPICS_DATABASE
                    if (topic['grade_min'] <= target_grade <= topic['grade_max'] and
                        topic['difficulty_min'] <= target_difficulty <= topic['difficulty_max'])
                ]
                
                if suitable_topics:
                    topic_obj = random.choice(suitable_topics)
                    topic_name = f"{topic_obj['category']}: {topic_obj['topic']}"
                else:
                    topic_name = "Математика: Общие задачи"
                
                self.stdout.write(f'   Тема: {topic_name}')
                self.stdout.write(f'   Класс: {target_grade}')
                self.stdout.write(f'   Сложность: {target_difficulty}')
                
                # Генерируем задачу
                problem_data = gemini.generate_problem(
                    topic=topic_name,
                    difficulty=target_difficulty,
                    user_level=target_difficulty,
                    user_grade=target_grade,
                    user_age=target_grade + 6  # Примерный возраст
                )
                
                # Сохраняем в БД
                with transaction.atomic():
                    problem = Problem.objects.create(
                        topic=None,
                        title=problem_data['title'],
                        latex_formula=problem_data.get('equation_to_solve', ''),
                        description=problem_data.get('problem_text', problem_data.get('description', '')),
                        correct_answer=problem_data['correct_answer'],
                        difficulty_score=problem_data['difficulty_score'],
                        solution_steps=problem_data.get('solution_steps', []),
                        hints=problem_data.get('hints', []),
                        grade_level=target_grade,
                        source='ai_generated',
                        times_used=0,
                        is_active=True
                    )
                
                success_count += 1
                self.stdout.write(self.style.SUCCESS(f'   ✅ Задача сохранена: ID={problem.id}'))
                
                # Задержка между запросами
                if i < count - 1:  # Не ждем после последней задачи
                    self.stdout.write(f'   ⏳ Ожидание {delay} сек...')
                    time.sleep(delay)
                
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'   ❌ Ошибка: {str(e)}'))
                continue
        
        # Итоговая статистика
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Генерация завершена!'))
        self.stdout.write(f'✅ Успешно: {success_count}')
        self.stdout.write(f'❌ Ошибок: {error_count}')
        self.stdout.write(f'📊 Всего задач в БД: {Problem.objects.count()}')
        self.stdout.write('\n' + '='*50 + '\n')
