"""
Book Importer Service - Импорт математических задач из книг
Поддерживает PDF, DOCX, TXT файлы с автоматической структуризацией через Gemini AI
"""

import logging
import os
import base64
from typing import Dict, List, Any, Optional
from pathlib import Path
from django.db import transaction
from django.core.files.uploadedfile import UploadedFile
from decouple import config
import google.generativeai as genai

from problems.models import Problem, Topic

logger = logging.getLogger(__name__)


class BookImporter:
    """
    Сервис для импорта математических задач из книг и сборников
    """
    
    def __init__(self):
        """Инициализация с Gemini API"""
        api_key = config('GEMINI_API_KEY', default=None)
        if not api_key:
            raise ValueError("GEMINI_API_KEY не установлен")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        logger.info("BookImporter инициализирован")
    
    def extract_problems_from_pdf(
        self,
        pdf_path: str,
        topic_name: Optional[str] = None,
        grade_level: Optional[int] = None,
        difficulty_range: tuple = (800, 1500)
    ) -> Dict[str, Any]:
        """
        Извлекает задачи из PDF файла используя Gemini
        
        Args:
            pdf_path: Путь к PDF файлу
            topic_name: Название темы (опционально)
            grade_level: Класс (опционально)
            difficulty_range: Диапазон сложности (min, max)
        
        Returns:
            Dict с результатами импорта
        """
        try:
            logger.info(f"Начало извлечения задач из PDF: {pdf_path}")
            
            # Сначала пробуем извлечь текст через pdfplumber
            try:
                import pdfplumber
                text_content = ""
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        text_content += page.extract_text() or ""
                
                if text_content.strip():
                    logger.info("Текст успешно извлечен через pdfplumber, используем текстовый метод")
                    return self.extract_problems_from_text(
                        text_content=text_content,
                        topic_name=topic_name,
                        grade_level=grade_level,
                        difficulty_range=difficulty_range
                    )
            except ImportError:
                logger.warning("pdfplumber не установлен, используем прямую отправку PDF в Gemini")
            except Exception as e:
                logger.warning(f"Не удалось извлечь текст через pdfplumber: {str(e)}, пробуем Gemini напрямую")
            
            # Загружаем PDF в Gemini
            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()
            
            # Кодируем в base64 для передачи
            pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
            
            # Создаем промпт для извлечения задач
            prompt = self._create_extraction_prompt(
                topic_name=topic_name,
                grade_level=grade_level
            )
            
            # Отправляем PDF в Gemini для анализа
            response = self.model.generate_content([
                {
                    'mime_type': 'application/pdf',
                    'data': pdf_base64
                },
                prompt
            ])
            
            # Парсим ответ от Gemini
            problems_data = self._parse_gemini_response(response.text)
            
            # Если не удалось извлечь задачи, логируем ответ для отладки
            if not problems_data:
                logger.warning(f"Gemini не смог извлечь задачи. Ответ: {response.text[:500]}")
            
            # Сохраняем задачи в БД
            results = self._save_problems_to_db(
                problems_data=problems_data,
                topic_name=topic_name,
                grade_level=grade_level,
                difficulty_range=difficulty_range,
                source_file=os.path.basename(pdf_path)
            )
            
            logger.info(f"Импорт завершен: {results['imported']}/{results['total']} задач")
            return results
            
        except Exception as e:
            logger.error(f"Ошибка при извлечении из PDF: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'total': 0,
                'imported': 0,
                'skipped': 0,
                'errors': []
            }
    
    def extract_problems_from_text(
        self,
        text_content: str,
        topic_name: Optional[str] = None,
        grade_level: Optional[int] = None,
        difficulty_range: tuple = (800, 1500)
    ) -> Dict[str, Any]:
        """
        Извлекает задачи из текстового содержимого
        
        Args:
            text_content: Текст с задачами
            topic_name: Название темы
            grade_level: Класс
            difficulty_range: Диапазон сложности
        
        Returns:
            Dict с результатами импорта
        """
        try:
            logger.info("Начало извлечения задач из текста")
            
            prompt = self._create_extraction_prompt(
                topic_name=topic_name,
                grade_level=grade_level
            )
            
            full_prompt = f"{prompt}\n\n**ТЕКСТ С ЗАДАЧАМИ:**\n{text_content}"
            
            response = self.model.generate_content(full_prompt)
            
            problems_data = self._parse_gemini_response(response.text)
            
            results = self._save_problems_to_db(
                problems_data=problems_data,
                topic_name=topic_name,
                grade_level=grade_level,
                difficulty_range=difficulty_range,
                source_file='text_input'
            )
            
            logger.info(f"Импорт из текста завершен: {results['imported']}/{results['total']} задач")
            return results
            
        except Exception as e:
            logger.error(f"Ошибка при извлечении из текста: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'total': 0,
                'imported': 0,
                'skipped': 0,
                'errors': []
            }
    
    def _create_extraction_prompt(
        self,
        topic_name: Optional[str] = None,
        grade_level: Optional[int] = None
    ) -> str:
        """
        Создает промпт для извлечения задач
        """
        topic_info = f"Тема: {topic_name}" if topic_name else "Тема: определить автоматически"
        grade_info = f"Класс: {grade_level}" if grade_level else "Класс: определить автоматически"
        
        prompt = f"""
Ты - эксперт по математике. Твоя задача - извлечь все математические задачи из документа и структурировать их.

**КОНТЕКСТ:**
{topic_info}
{grade_info}

**ИНСТРУКЦИИ:**
1. Найди все математические задачи в документе
2. Для каждой задачи извлеки:
   - Номер задачи (если есть)
   - Полное условие задачи
   - LaTeX формулу (если есть формулы в условии)
   - Правильный ответ (если указан)
   - Решение (если есть)
   - Подсказки (если есть)
   - Тему/раздел математики
   - Примерную сложность (0-3000)
   - Класс (1-12)

**ФОРМАТ ВЫВОДА:**
Верни ТОЛЬКО JSON массив, без дополнительного текста. Формат:

```json
[
  {{
    "number": "1",
    "title": "Краткое название задачи",
    "description": "Полное условие задачи",
    "latex_formula": "LaTeX формула (если есть)",
    "correct_answer": "Правильный ответ",
    "solution_steps": [
      "Шаг 1: описание",
      "Шаг 2: описание"
    ],
    "hints": ["Подсказка 1", "Подсказка 2"],
    "topic": "Название темы (например: Алгебра: Квадратные уравнения)",
    "difficulty_score": 1200,
    "grade_level": 9
  }}
]
```

**КРИТИЧЕСКИ ВАЖНО:**
- Извлекай ВСЕ задачи из документа (даже если их много)
- Каждая задача должна быть отдельным объектом в массиве
- Если информация отсутствует, используй пустую строку ""
- Для LaTeX используй правильный синтаксис
- Оценивай сложность реалистично (легкие: 500-900, средние: 1000-1500, сложные: 1600-2500)
- Определяй класс по сложности задачи
- НЕ добавляй никакого текста до или после JSON
- Убедись что JSON валидный и может быть распарсен

Начинай извлечение задач СЕЙЧАС:
"""
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Парсит ответ от Gemini и извлекает JSON с задачами
        """
        import json
        import re
        
        try:
            # Ищем JSON в ответе (с или без маркеров ```json)
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
            else:
                # Пробуем найти массив напрямую
                json_match = re.search(r'\[\s*\{[\s\S]*\}\s*\]', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    # Последняя попытка - весь текст может быть JSON
                    json_str = response_text.strip()
            
            # Пробуем распарсить
            try:
                problems = json.loads(json_str)
            except json.JSONDecodeError:
                # Если не получилось, пробуем найти и исправить частичный JSON
                # Ищем начало массива и пытаемся найти все объекты
                objects = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', json_str, re.DOTALL)
                if objects:
                    problems = []
                    for obj_str in objects:
                        try:
                            obj = json.loads(obj_str)
                            problems.append(obj)
                        except:
                            continue
                    if not problems:
                        logger.warning("Не удалось извлечь задачи из ответа")
                        logger.debug(f"Ответ Gemini (первые 1000 символов): {response_text[:1000]}")
                        return []
                else:
                    logger.warning("JSON не найден в ответе Gemini")
                    logger.debug(f"Ответ Gemini (первые 1000 символов): {response_text[:1000]}")
                    return []
            
            if not isinstance(problems, list):
                problems = [problems]
            
            logger.info(f"Извлечено {len(problems)} задач из ответа Gemini")
            return problems
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге ответа: {str(e)}")
            logger.debug(f"Ответ Gemini (первые 1000 символов): {response_text[:1000]}")
            return []
    
    def _save_problems_to_db(
        self,
        problems_data: List[Dict[str, Any]],
        topic_name: Optional[str],
        grade_level: Optional[int],
        difficulty_range: tuple,
        source_file: str
    ) -> Dict[str, Any]:
        """
        Сохраняет извлеченные задачи в БД
        """
        results = {
            'success': True,
            'total': len(problems_data),
            'imported': 0,
            'skipped': 0,
            'errors': []
        }
        
        for idx, problem_data in enumerate(problems_data, 1):
            try:
                with transaction.atomic():
                    # Получаем или создаем тему
                    topic_name_final = problem_data.get('topic') or topic_name or 'Общая математика'
                    topic, _ = Topic.objects.get_or_create(
                        name=topic_name_final,
                        defaults={
                            'description': f'Автоматически создано при импорте из {source_file}',
                            'difficulty_base': difficulty_range[0]
                        }
                    )
                    
                    # Определяем сложность
                    difficulty = problem_data.get('difficulty_score', difficulty_range[0])
                    if difficulty < difficulty_range[0]:
                        difficulty = difficulty_range[0]
                    elif difficulty > difficulty_range[1]:
                        difficulty = difficulty_range[1]
                    
                    # Определяем класс
                    grade = problem_data.get('grade_level') or grade_level
                    if not grade:
                        # Определяем класс по сложности
                        if difficulty <= 600:
                            grade = 5
                        elif difficulty <= 900:
                            grade = 7
                        elif difficulty <= 1200:
                            grade = 9
                        elif difficulty <= 1500:
                            grade = 10
                        else:
                            grade = 11
                    
                    # Формируем заголовок
                    title = problem_data.get('title', '').strip()
                    if not title:
                        number = problem_data.get('number', idx)
                        title = f"Задача {number} - {topic_name_final}"
                    
                    # Создаем задачу
                    problem = Problem.objects.create(
                        topic=topic,
                        title=title[:300],
                        latex_formula=problem_data.get('latex_formula', ''),
                        description=problem_data.get('description', ''),
                        correct_answer=problem_data.get('correct_answer', ''),
                        difficulty_score=difficulty,
                        solution_steps=problem_data.get('solution_steps', []),
                        hints=problem_data.get('hints', []),
                        grade_level=grade,
                        source='imported',
                        is_active=True
                    )
                    
                    results['imported'] += 1
                    logger.debug(f"Задача {idx} импортирована: {title}")
                    
            except Exception as e:
                results['errors'].append({
                    'problem_number': idx,
                    'error': str(e)
                })
                logger.error(f"Ошибка при сохранении задачи {idx}: {str(e)}")
        
        results['skipped'] = results['total'] - results['imported']
        return results
    
    def import_from_uploaded_file(
        self,
        uploaded_file: UploadedFile,
        topic_name: Optional[str] = None,
        grade_level: Optional[int] = None,
        difficulty_range: tuple = (800, 1500)
    ) -> Dict[str, Any]:
        """
        Импортирует задачи из загруженного файла
        
        Args:
            uploaded_file: Загруженный файл (PDF, TXT, DOCX)
            topic_name: Название темы
            grade_level: Класс
            difficulty_range: Диапазон сложности
        
        Returns:
            Dict с результатами импорта
        """
        try:
            file_extension = Path(uploaded_file.name).suffix.lower()
            
            # Сохраняем временно файл
            temp_dir = Path('media/temp_books')
            temp_dir.mkdir(parents=True, exist_ok=True)
            temp_file_path = temp_dir / uploaded_file.name
            
            with open(temp_file_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            
            # Обрабатываем в зависимости от типа
            if file_extension == '.pdf':
                results = self.extract_problems_from_pdf(
                    pdf_path=str(temp_file_path),
                    topic_name=topic_name,
                    grade_level=grade_level,
                    difficulty_range=difficulty_range
                )
            elif file_extension in ['.txt', '.md']:
                with open(temp_file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                results = self.extract_problems_from_text(
                    text_content=text_content,
                    topic_name=topic_name,
                    grade_level=grade_level,
                    difficulty_range=difficulty_range
                )
            else:
                return {
                    'success': False,
                    'error': f'Неподдерживаемый формат файла: {file_extension}',
                    'total': 0,
                    'imported': 0
                }
            
            # Удаляем временный файл
            temp_file_path.unlink(missing_ok=True)
            
            return results
            
        except Exception as e:
            logger.error(f"Ошибка при импорте из файла: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'total': 0,
                'imported': 0
            }


# Глобальный экземпляр
_book_importer = None


def get_book_importer() -> BookImporter:
    """Получить глобальный экземпляр BookImporter"""
    global _book_importer
    if _book_importer is None:
        _book_importer = BookImporter()
    return _book_importer
