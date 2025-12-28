"""
Management команда для импорта задач из книг
"""

from django.core.management.base import BaseCommand
from core.book_importer import get_book_importer
from pathlib import Path


class Command(BaseCommand):
    help = 'Импортирует математические задачи из книги (PDF, TXT)'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Путь к файлу с задачами (PDF или TXT)'
        )
        parser.add_argument(
            '--topic',
            type=str,
            default=None,
            help='Название темы (опционально)'
        )
        parser.add_argument(
            '--grade',
            type=int,
            default=None,
            help='Класс (1-12, опционально)'
        )
        parser.add_argument(
            '--min-difficulty',
            type=int,
            default=800,
            help='Минимальная сложность (по умолчанию: 800)'
        )
        parser.add_argument(
            '--max-difficulty',
            type=int,
            default=1500,
            help='Максимальная сложность (по умолчанию: 1500)'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        topic = options['topic']
        grade = options['grade']
        min_diff = options['min_difficulty']
        max_diff = options['max_difficulty']
        
        # Проверяем существование файла
        if not Path(file_path).exists():
            self.stdout.write(self.style.ERROR(f'❌ Файл не найден: {file_path}'))
            return
        
        self.stdout.write(self.style.WARNING(f'📚 Начинаем импорт из: {file_path}'))
        if topic:
            self.stdout.write(f'   Тема: {topic}')
        if grade:
            self.stdout.write(f'   Класс: {grade}')
        self.stdout.write(f'   Диапазон сложности: {min_diff}-{max_diff}')
        self.stdout.write('')
        
        try:
            importer = get_book_importer()
            
            # Определяем тип файла
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.pdf':
                self.stdout.write('📄 Обработка PDF файла...')
                results = importer.extract_problems_from_pdf(
                    pdf_path=file_path,
                    topic_name=topic,
                    grade_level=grade,
                    difficulty_range=(min_diff, max_diff)
                )
            elif file_extension in ['.txt', '.md']:
                self.stdout.write('📝 Обработка текстового файла...')
                with open(file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                results = importer.extract_problems_from_text(
                    text_content=text_content,
                    topic_name=topic,
                    grade_level=grade,
                    difficulty_range=(min_diff, max_diff)
                )
            else:
                self.stdout.write(self.style.ERROR(
                    f'❌ Неподдерживаемый формат: {file_extension}'
                ))
                return
            
            # Выводим результаты
            self.stdout.write('')
            if results.get('success', False):
                self.stdout.write(self.style.SUCCESS(
                    f'✅ Импорт завершен успешно!'
                ))
                self.stdout.write(f'   Всего задач найдено: {results["total"]}')
                self.stdout.write(f'   Импортировано: {results["imported"]}')
                if results['skipped'] > 0:
                    self.stdout.write(f'   Пропущено: {results["skipped"]}')
                
                if results.get('errors'):
                    self.stdout.write(self.style.WARNING(
                        f'\n⚠️  Ошибки при импорте некоторых задач:'
                    ))
                    for error in results['errors'][:5]:  # Показываем первые 5
                        self.stdout.write(
                            f'   - Задача #{error["problem_number"]}: {error["error"]}'
                        )
            else:
                self.stdout.write(self.style.ERROR(
                    f'❌ Ошибка импорта: {results.get("error", "Unknown")}'
                ))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Критическая ошибка: {str(e)}'))
