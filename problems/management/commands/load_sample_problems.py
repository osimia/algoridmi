from django.core.management.base import BaseCommand
from problems.models import Topic, Problem


class Command(BaseCommand):
    help = 'Загружает примеры задач в базу данных'
    
    def handle(self, *args, **options):
        self.stdout.write('Загрузка примеров задач...')
        
        # Создаем темы
        topics_data = [
            {
                'name': 'Алгебра: Иррациональные уравнения',
                'description': 'Решение уравнений с корнями',
                'difficulty_base': 1200
            },
            {
                'name': 'Теория чисел: Сравнение по модулю',
                'description': 'Работа с модульной арифметикой',
                'difficulty_base': 1400
            },
            {
                'name': 'Геометрия: Вписанные углы',
                'description': 'Задачи на вписанные углы в окружности',
                'difficulty_base': 1100
            },
            {
                'name': 'Алгебра: Квадратные уравнения',
                'description': 'Решение квадратных уравнений',
                'difficulty_base': 800
            },
            {
                'name': 'Комбинаторика: Перестановки',
                'description': 'Подсчет перестановок и сочетаний',
                'difficulty_base': 1300
            },
        ]
        
        topics = {}
        for topic_data in topics_data:
            topic, created = Topic.objects.get_or_create(
                name=topic_data['name'],
                defaults={
                    'description': topic_data['description'],
                    'difficulty_base': topic_data['difficulty_base']
                }
            )
            topics[topic_data['name']] = topic
            if created:
                self.stdout.write(f'  Создана тема: {topic.name}')
        
        # Создаем задачи
        problems_data = [
            {
                'topic': 'Алгебра: Иррациональные уравнения',
                'title': 'Иррациональное уравнение с квадратным корнем',
                'latex_formula': r'\sqrt{3x + 1} = x - 1',
                'description': 'Найдите сумму квадратов корней уравнения, которые удовлетворяют условию x > 0.',
                'correct_answer': '25',
                'difficulty_score': 1200,
                'solution_steps': [
                    'Шаг 1: Определяем ОДЗ: 3x + 1 ≥ 0 и x - 1 ≥ 0, откуда x ≥ 1',
                    'Шаг 2: Возводим обе части в квадрат: 3x + 1 = (x - 1)²',
                    'Шаг 3: Раскрываем скобки: 3x + 1 = x² - 2x + 1',
                    'Шаг 4: Переносим все в одну сторону: x² - 5x = 0',
                    'Шаг 5: Факторизуем: x(x - 5) = 0',
                    'Шаг 6: Находим корни: x₁ = 0, x₂ = 5',
                    'Шаг 7: Проверяем по ОДЗ: x = 0 не подходит, x = 5 подходит',
                    'Шаг 8: Сумма квадратов: 5² = 25'
                ],
                'hints': [
                    'Не забудьте про область допустимых значений!',
                    'После возведения в квадрат всегда проверяйте корни'
                ]
            },
            {
                'topic': 'Алгебра: Квадратные уравнения',
                'title': 'Простое квадратное уравнение',
                'latex_formula': r'x^2 - 7x + 12 = 0',
                'description': 'Решите квадратное уравнение и найдите произведение его корней.',
                'correct_answer': '12',
                'difficulty_score': 800,
                'solution_steps': [
                    'Шаг 1: Используем теорему Виета: произведение корней = c/a',
                    'Шаг 2: В нашем случае: 12/1 = 12',
                    'Альтернативно: факторизация (x - 3)(x - 4) = 0',
                    'Корни: x₁ = 3, x₂ = 4',
                    'Произведение: 3 × 4 = 12'
                ],
                'hints': ['Вспомните теорему Виета', 'Попробуйте факторизацию']
            },
            {
                'topic': 'Геометрия: Вписанные углы',
                'title': 'Вписанный угол и центральный угол',
                'latex_formula': r'\angle ACB = 30°',
                'description': 'Вписанный угол ACB опирается на дугу AB. Найдите величину центрального угла AOB (в градусах).',
                'correct_answer': '60',
                'difficulty_score': 1100,
                'solution_steps': [
                    'Шаг 1: Вспоминаем теорему: вписанный угол равен половине центрального',
                    'Шаг 2: Центральный угол = 2 × вписанный угол',
                    'Шаг 3: AOB = 2 × 30° = 60°'
                ],
                'hints': ['Вписанный угол в два раза меньше центрального']
            },
            {
                'topic': 'Теория чисел: Сравнение по модулю',
                'title': 'Остаток от деления',
                'latex_formula': r'2^{10} \pmod{7}',
                'description': 'Найдите остаток от деления 2¹⁰ на 7.',
                'correct_answer': '2',
                'difficulty_score': 1400,
                'solution_steps': [
                    'Шаг 1: Вычисляем степени двойки по модулю 7',
                    'Шаг 2: 2¹ ≡ 2 (mod 7)',
                    'Шаг 3: 2² ≡ 4 (mod 7)',
                    'Шаг 4: 2³ ≡ 8 ≡ 1 (mod 7)',
                    'Шаг 5: Период повторяется каждые 3 степени',
                    'Шаг 6: 10 = 3×3 + 1',
                    'Шаг 7: 2¹⁰ ≡ 2¹ ≡ 2 (mod 7)'
                ],
                'hints': ['Ищите периодичность', 'Используйте свойства модульной арифметики']
            },
            {
                'topic': 'Комбинаторика: Перестановки',
                'title': 'Количество перестановок',
                'latex_formula': r'P(5)',
                'description': 'Сколькими способами можно расставить 5 различных книг на полке?',
                'correct_answer': '120',
                'difficulty_score': 1300,
                'solution_steps': [
                    'Шаг 1: Используем формулу перестановок: P(n) = n!',
                    'Шаг 2: P(5) = 5!',
                    'Шаг 3: 5! = 5 × 4 × 3 × 2 × 1 = 120'
                ],
                'hints': ['Используйте факториал', 'n! = n × (n-1) × ... × 1']
            },
        ]
        
        created_count = 0
        for problem_data in problems_data:
            topic = topics[problem_data['topic']]
            problem, created = Problem.objects.get_or_create(
                title=problem_data['title'],
                topic=topic,
                defaults={
                    'latex_formula': problem_data['latex_formula'],
                    'description': problem_data['description'],
                    'correct_answer': problem_data['correct_answer'],
                    'difficulty_score': problem_data['difficulty_score'],
                    'solution_steps': problem_data['solution_steps'],
                    'hints': problem_data['hints'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  Создана задача: {problem.title}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Загрузка завершена! Создано задач: {created_count}'
            )
        )
