"""
Views для работы с задачами через Gemini API
Генерация задач и проверка решений с помощью ИИ
"""

import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
import random
from .models import UserAttempt, Topic
from core.gemini_service import get_gemini_service
from core.math_topics_database import get_random_topic_for_grade, get_topic_by_difficulty

# Настройка логирования
logger = logging.getLogger(__name__)

# Thread pool для параллельной генерации задач
# max_workers=5 означает максимум 5 одновременных генераций
executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="GeminiGen")


def _get_difficulty_level(score):
    """Определяет уровень сложности по баллам"""
    if score <= 300:
        return "Начальный"
    elif score <= 600:
        return "Легкий"
    elif score <= 900:
        return "Средний"
    elif score <= 1200:
        return "Выше среднего"
    elif score <= 1500:
        return "Сложный"
    elif score <= 2000:
        return "Очень сложный"
    else:
        return "Экспертный"


def _get_estimated_time(score):
    """Определяет примерное время решения в минутах"""
    if score <= 300:
        return "2-3 минуты"
    elif score <= 600:
        return "3-5 минут"
    elif score <= 900:
        return "5-8 минут"
    elif score <= 1200:
        return "8-12 минут"
    elif score <= 1500:
        return "12-15 минут"
    elif score <= 2000:
        return "15-20 минут"
    else:
        return "20+ минут"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_problem_ai(request):
    """
    Генерация новой задачи через Gemini API
    GET /api/problems/generate-ai/
    
    Параметры:
    - topic (optional): Название темы
    """
    user = request.user
    # Получаем профиль пользователя
    profile = user.profile
    
    # Проверяем заполненность профиля
    if not profile.is_profile_complete:
        return Response({
            'error': 'Профиль не заполнен',
            'message': 'Пожалуйста, заполните профиль перед решением задач',
            'profile_incomplete': True
        }, status=status.HTTP_403_FORBIDDEN)
    
    user_index = profile.al_khwarizmi_index
    
    # Используем рекомендуемую сложность на основе класса/возраста
    recommended_diff = profile.recommended_difficulty
    
    # Определяем диапазон сложности задач
    min_difficulty = max(0, recommended_diff - 150)
    max_difficulty = min(3000, recommended_diff + 150)
    target_difficulty = recommended_diff
    
    # Получаем тему из базы данных 1010+ тем
    topic_param = request.query_params.get('topic')
    
    if topic_param:
        topic_name = topic_param
    else:
        # Используем базу данных из 1010+ тем
        # Выбираем тему по классу и сложности
        if profile.grade:
            topic_obj = get_random_topic_for_grade(profile.grade)
            if topic_obj:
                topic_name = f"{topic_obj['category']}: {topic_obj['topic']}"
                # Корректируем сложность на основе темы
                target_difficulty = (topic_obj['difficulty_min'] + topic_obj['difficulty_max']) // 2
                logger.info(f"📚 Выбрана тема из базы: {topic_name} | Сложность: {target_difficulty}")
            else:
                # Fallback на старую систему
                topic_name = "Математика: Общие задачи"
        else:
            # Если класс не указан, выбираем по сложности
            topic_obj = get_topic_by_difficulty(target_difficulty)
            if topic_obj:
                topic_name = f"{topic_obj['category']}: {topic_obj['topic']}"
                logger.info(f"📚 Выбрана тема по сложности: {topic_name}")
            else:
                topic_name = "Математика: Общие задачи"
    
    # Логируем запрос
    logger.info(f"📝 Запрос генерации задачи | Пользователь: {user.username} (ID: {user.id}) | Тема: {topic_name} | Сложность: {target_difficulty}")
    
    try:
        # Получаем сервис Gemini
        gemini = get_gemini_service()
        
        # Функция для генерации в отдельном потоке
        def generate_task():
            return gemini.generate_problem(
                topic=topic_name,
                difficulty=target_difficulty,
                user_level=user_index,
                user_grade=profile.grade,
                user_age=profile.age
            )
        
        # Запускаем генерацию в thread pool с таймаутом 30 секунд
        logger.info(f"🔄 Отправка задачи в thread pool | Активных потоков: {executor._threads.__len__() if hasattr(executor, '_threads') else 'N/A'}")
        future = executor.submit(generate_task)
        
        try:
            # Ждем результат максимум 30 секунд
            problem_data = future.result(timeout=30)
            logger.info(f"✅ Задача получена из thread pool | Пользователь: {user.username}")
        except FuturesTimeoutError:
            logger.error(f"⏰ Таймаут генерации задачи (30 сек) | Пользователь: {user.username}")
            return Response({
                'error': 'Генерация задачи заняла слишком много времени. Попробуйте еще раз.'
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
        
        # Сохраняем задачу в кеше для последующей проверки
        # Ключ: user_id + timestamp (без кириллицы для совместимости с memcached)
        import hashlib
        title_hash = hashlib.md5(problem_data.get('title', 'temp').encode()).hexdigest()[:8]
        cache_key = f"problem_{user.id}_{title_hash}"
        cache.set(cache_key, problem_data, timeout=3600)  # 1 час
        
        # Возвращаем задачу БЕЗ правильного ответа и БЕЗ формулы решения
        # Используем плоскую структуру для совместимости с фронтендом
        problem_text = problem_data.get('problem_text') or problem_data.get('description') or problem_data.get('title', 'Задача генерируется...')
        
        # Получаем уравнение, если есть
        equation = problem_data.get('equation_to_solve', '') or ''
        
        problem_response = {
            'id': cache_key,
            'topic_name': topic_name,
            'title': problem_data['title'],
            'description': problem_text,
            'difficulty_score': problem_data['difficulty_score'],
            'hints': problem_data.get('hints', []),
            'generated_by_ai': True
        }
        
        # Добавляем latex_formula только если есть уравнение
        if equation and equation.strip():
            problem_response['latex_formula'] = equation
        
        response_data = {
            'problem': problem_response,
            'user_index': user_index,
            'difficulty_range': {
                'min': min_difficulty,
                'max': max_difficulty
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except ValueError as e:
        logger.error(f"❌ ValueError при генерации | Пользователь: {user.username} | Ошибка: {str(e)}")
        return Response({
            'error': f'Ошибка генерации задачи: {str(e)}',
            'detail': 'Проверьте настройки GEMINI_API_KEY'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка | Пользователь: {user.username} | Ошибка: {str(e)}")
        return Response({
            'error': f'Ошибка: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer_ai(request):
    """
    Отправка ответа на задачу с проверкой через Gemini API
    POST /api/problems/submit-ai/
    
    Body:
    - problem_id: ID задачи (cache_key)
    - submitted_answer: Ответ пользователя
    - solution_photo: Фото решения (опционально)
    """
    user = request.user
    
    # Логируем начало проверки
    logger.info(f"📤 Запрос проверки ответа | Пользователь: {user.username} (ID: {user.id})")
    logger.debug(f"Request data: {request.data}")
    logger.debug(f"Request FILES: {request.FILES}")
    
    problem_id = request.data.get('problem_id')
    submitted_answer = request.data.get('submitted_answer', '').strip()
    solution_photo = request.FILES.get('solution_photo')
    
    logger.info(f"📋 Данные запроса | problem_id: {problem_id} | answer: '{submitted_answer}' | has_photo: {bool(solution_photo)}")
    
    if not problem_id:
        logger.warning(f"⚠️  Отсутствует problem_id | Пользователь: {user.username}")
        return Response({
            'error': 'Требуется problem_id'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not submitted_answer and not solution_photo:
        logger.warning(f"⚠️  Нет ответа и фото | Пользователь: {user.username}")
        return Response({
            'error': 'Требуется ответ или фото решения'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Получаем задачу из кеша
    logger.info(f"🔍 Поиск задачи в кеше | cache_key: {problem_id}")
    problem_data = cache.get(problem_id)
    
    if not problem_data:
        logger.error(f"❌ Задача не найдена в кеше | cache_key: {problem_id} | Пользователь: {user.username}")
        return Response({
            'error': 'Задача не найдена или истекло время',
            'detail': 'Пожалуйста, сгенерируйте новую задачу'
        }, status=status.HTTP_404_NOT_FOUND)
    
    logger.info(f"✅ Задача найдена | Название: '{problem_data.get('title')}' | Правильный ответ: {problem_data.get('correct_answer')}")
    
    try:
        # Получаем сервис Gemini
        logger.info(f"🤖 Запуск проверки через Gemini AI")
        gemini = get_gemini_service()
        
        # Проверяем решение через ИИ
        logger.info(f"🔄 Отправка на проверку | Ответ пользователя: '{submitted_answer}' | Правильный: '{problem_data.get('correct_answer')}'")
        check_result = gemini.check_solution(
            problem_data=problem_data,
            user_answer=submitted_answer,
            solution_photo=solution_photo.path if solution_photo else None
        )
        
        is_correct = check_result['is_correct']
        confidence = check_result.get('confidence', 0.9)
        
        logger.info(f"✅ Результат проверки | Правильно: {is_correct} | Уверенность: {confidence}")
        
        # Определяем очки
        if solution_photo:
            points_awarded = 250 if is_correct else 50
        else:
            points_awarded = 150 if is_correct else 0
        
        # Создаем запись о попытке
        attempt = UserAttempt.objects.create(
            user=user,
            problem=None,  # Нет связи с Problem из БД
            submitted_answer=submitted_answer or 'Фото решения',
            is_correct=is_correct,
            points_awarded=points_awarded,
            solution_photo=solution_photo,
            ai_analysis={
                'gemini_check': check_result,
                'problem_data': {
                    'title': problem_data['title'],
                    'difficulty': problem_data['difficulty_score']
                }
            }
        )
        
        # Обновляем индекс пользователя
        index_change = user.profile.update_index(
            problem_data['difficulty_score'],
            is_correct
        )
        
        # Обновляем weekly_score в арене
        from arena.models import ArenaRank
        arena_rank, created = ArenaRank.objects.get_or_create(
            user=user,
            defaults={
                'current_index': user.profile.al_khwarizmi_index,
                'current_division': ArenaRank.get_division_from_index(
                    user.profile.al_khwarizmi_index
                )
            }
        )
        if is_correct:
            arena_rank.weekly_score += points_awarded
            arena_rank.current_index = user.profile.al_khwarizmi_index
            arena_rank.current_division = ArenaRank.get_division_from_index(
                user.profile.al_khwarizmi_index
            )
            arena_rank.save()
            arena_rank.update_rank()  # Обновляем место в рейтинге
        
        # Формируем ответ
        response_data = {
            'is_correct': is_correct,
            'points_awarded': points_awarded,
            'index_change': index_change,
            'new_index': user.profile.al_khwarizmi_index,
            'correct_answer': problem_data['correct_answer'],
            'solution_steps': problem_data.get('solution_steps', []),
            'ai_feedback': check_result.get('feedback', ''),
            'confidence': confidence,
            'attempt_id': attempt.id
        }
        
        logger.info(f"💾 Сохранение результата | Пользователь: {user.username} | Очки: {points_awarded} | Изменение индекса: {index_change}")
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при проверке решения | Пользователь: {user.username} | Ошибка: {str(e)}")
        logger.exception("Полный traceback:")
        return Response({
            'error': f'Ошибка проверки решения: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_topics(request):
    """
    Получение списка доступных тем для генерации
    GET /api/problems/topics-ai/
    """
    topics = Topic.objects.all().values('id', 'name', 'description', 'difficulty_base')
    
    # Добавляем дополнительные темы, которые может генерировать ИИ
    ai_topics = [
        {
            'id': 'ai_algebra',
            'name': 'Алгебра: Смешанные задачи',
            'description': 'Различные алгебраические задачи, генерируемые ИИ',
            'difficulty_base': 1000
        },
        {
            'id': 'ai_geometry',
            'name': 'Геометрия: Смешанные задачи',
            'description': 'Различные геометрические задачи, генерируемые ИИ',
            'difficulty_base': 1200
        },
        {
            'id': 'ai_calculus',
            'name': 'Математический анализ',
            'description': 'Задачи по производным, интегралам и пределам',
            'difficulty_base': 1500
        },
        {
            'id': 'ai_probability',
            'name': 'Теория вероятностей',
            'description': 'Задачи на вероятность и статистику',
            'difficulty_base': 1300
        }
    ]
    
    return Response({
        'db_topics': list(topics),
        'ai_topics': ai_topics
    }, status=status.HTTP_200_OK)
