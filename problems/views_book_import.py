"""
Views для импорта задач из книг
"""

import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

from core.book_importer import get_book_importer

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def upload_and_import_book(request):
    """
    Загрузить книгу и импортировать задачи (только для админов)
    
    Form data:
    - file: PDF или TXT файл
    - topic: название темы (опционально)
    - grade: класс 1-12 (опционально)
    - min_difficulty: минимальная сложность (по умолчанию 800)
    - max_difficulty: максимальная сложность (по умолчанию 1500)
    """
    try:
        # Проверяем наличие файла
        if 'file' not in request.FILES:
            return Response({
                'success': False,
                'error': 'Файл не предоставлен'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES['file']
        topic = request.data.get('topic')
        grade = request.data.get('grade')
        min_diff = int(request.data.get('min_difficulty', 800))
        max_diff = int(request.data.get('max_difficulty', 1500))
        
        # Валидация
        if grade:
            grade = int(grade)
            if grade < 1 or grade > 12:
                return Response({
                    'success': False,
                    'error': 'Класс должен быть от 1 до 12'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        logger.info(f"Импорт из файла: {uploaded_file.name}")
        
        # Импортируем задачи
        importer = get_book_importer()
        results = importer.import_from_uploaded_file(
            uploaded_file=uploaded_file,
            topic_name=topic,
            grade_level=grade,
            difficulty_range=(min_diff, max_diff)
        )
        
        if results.get('success', False):
            return Response({
                'success': True,
                'message': f'Импортировано {results["imported"]} из {results["total"]} задач',
                'results': {
                    'total': results['total'],
                    'imported': results['imported'],
                    'skipped': results['skipped'],
                    'errors': results.get('errors', [])
                }
            })
        else:
            return Response({
                'success': False,
                'error': results.get('error', 'Неизвестная ошибка'),
                'results': results
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"Ошибка при импорте книги: {str(e)}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def import_from_text(request):
    """
    Импортировать задачи из текста (только для админов)
    
    Body:
    {
        "text": "текст с задачами",
        "topic": "название темы",
        "grade": 9,
        "min_difficulty": 800,
        "max_difficulty": 1500
    }
    """
    try:
        text_content = request.data.get('text', '').strip()
        
        if not text_content:
            return Response({
                'success': False,
                'error': 'Текст не может быть пустым'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        topic = request.data.get('topic')
        grade = request.data.get('grade')
        min_diff = int(request.data.get('min_difficulty', 800))
        max_diff = int(request.data.get('max_difficulty', 1500))
        
        if grade:
            grade = int(grade)
            if grade < 1 or grade > 12:
                return Response({
                    'success': False,
                    'error': 'Класс должен быть от 1 до 12'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        logger.info("Импорт задач из текста")
        
        importer = get_book_importer()
        results = importer.extract_problems_from_text(
            text_content=text_content,
            topic_name=topic,
            grade_level=grade,
            difficulty_range=(min_diff, max_diff)
        )
        
        if results.get('success', False):
            return Response({
                'success': True,
                'message': f'Импортировано {results["imported"]} из {results["total"]} задач',
                'results': {
                    'total': results['total'],
                    'imported': results['imported'],
                    'skipped': results['skipped'],
                    'errors': results.get('errors', [])
                }
            })
        else:
            return Response({
                'success': False,
                'error': results.get('error', 'Неизвестная ошибка'),
                'results': results
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"Ошибка при импорте из текста: {str(e)}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def import_statistics(request):
    """
    Получить статистику импортированных задач
    """
    try:
        from problems.models import Problem
        from django.db.models import Count
        
        # Общая статистика
        total_imported = Problem.objects.filter(source='imported').count()
        
        # По темам
        by_topic = Problem.objects.filter(source='imported').values(
            'topic__name'
        ).annotate(count=Count('id')).order_by('-count')[:10]
        
        # По классам
        by_grade = Problem.objects.filter(source='imported').values(
            'grade_level'
        ).annotate(count=Count('id')).order_by('grade_level')
        
        # По сложности
        difficulty_ranges = [
            ('Легкие (0-800)', 0, 800),
            ('Средние (800-1200)', 800, 1200),
            ('Сложные (1200-1600)', 1200, 1600),
            ('Очень сложные (1600+)', 1600, 3000)
        ]
        
        by_difficulty = []
        for label, min_d, max_d in difficulty_ranges:
            count = Problem.objects.filter(
                source='imported',
                difficulty_score__gte=min_d,
                difficulty_score__lt=max_d
            ).count()
            by_difficulty.append({
                'range': label,
                'count': count
            })
        
        return Response({
            'success': True,
            'statistics': {
                'total_imported': total_imported,
                'by_topic': list(by_topic),
                'by_grade': list(by_grade),
                'by_difficulty': by_difficulty
            }
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении статистики: {str(e)}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
