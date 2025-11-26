from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
import random
from .models import Problem, UserAttempt, Topic
from .serializers import (
    ProblemSerializer, ProblemDetailSerializer,
    SubmitAnswerSerializer, UserAttemptSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_problem(request):
    """
    Генерация новой задачи для пользователя на основе его индекса.
    GET /api/problems/generate/
    
    Параметры:
    - topic_id (optional): ID конкретной темы
    """
    user = request.user
    profile = user.profile
    
    # Проверяем заполненность профиля
    if not profile.is_profile_complete:
        return Response({
            'error': 'Профиль не заполнен',
            'message': 'Пожалуйста, заполните профиль перед решением задач',
            'profile_incomplete': True
        }, status=status.HTTP_403_FORBIDDEN)
    
    user_index = profile.al_khwarizmi_index
    
    # Диапазон сложности: [Index - 100, Index + 50]
    min_difficulty = max(0, user_index - 100)
    max_difficulty = min(3000, user_index + 50)
    
    # Фильтр по теме (опционально)
    topic_id = request.query_params.get('topic_id')
    
    # Базовый запрос
    problems_query = Problem.objects.filter(
        is_active=True,
        difficulty_score__gte=min_difficulty,
        difficulty_score__lte=max_difficulty
    )
    
    if topic_id:
        problems_query = problems_query.filter(topic_id=topic_id)
    
    # Получаем список задач
    problems = list(problems_query)
    
    if not problems:
        # Если нет подходящих задач, расширяем диапазон
        problems = list(Problem.objects.filter(is_active=True))
    
    if not problems:
        return Response({
            'error': 'Нет доступных задач'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Выбираем случайную задачу
    problem = random.choice(problems)
    
    # Возвращаем задачу без правильного ответа и решения
    serializer = ProblemSerializer(problem)
    
    return Response({
        'problem': serializer.data,
        'user_index': user_index,
        'difficulty_range': {
            'min': min_difficulty,
            'max': max_difficulty
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request):
    """
    Отправка ответа на задачу.
    POST /api/problems/submit/
    
    Body:
    - problem_id: ID задачи
    - submitted_answer: Ответ пользователя (опционально)
    - solution_photo: Фото решения (опционально)
    - time_spent_seconds: Время решения в секундах (опционально)
    """
    serializer = SubmitAnswerSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    problem_id = serializer.validated_data['problem_id']
    submitted_answer = serializer.validated_data.get('submitted_answer', '').strip()
    solution_photo = serializer.validated_data.get('solution_photo')
    time_spent = serializer.validated_data.get('time_spent_seconds')
    
    # Получаем задачу
    problem = get_object_or_404(Problem, id=problem_id)
    
    # Проверка ответа
    is_correct = False
    points_awarded = 0
    
    if submitted_answer:
        # Нормализуем ответы для сравнения
        correct_normalized = problem.correct_answer.strip().lower().replace(' ', '')
        submitted_normalized = submitted_answer.lower().replace(' ', '')
        is_correct = correct_normalized == submitted_normalized
    
    # Если есть фото, симулируем анализ ИИ
    ai_analysis = None
    if solution_photo:
        # В реальной системе здесь был бы вызов AI сервиса
        # Для демонстрации используем простую логику
        ai_analysis = {
            'analyzed': True,
            'confidence': 0.95 if is_correct else 0.85,
            'detected_steps': ['Шаг 1: Определение ОДЗ', 'Шаг 2: Возведение в квадрат'],
            'errors_found': [] if is_correct else ['Не проверено условие ОДЗ']
        }
        
        # Если фото предоставлено и ответ правильный, больше очков
        if is_correct:
            points_awarded = 250
        else:
            points_awarded = 50  # Частичные очки за попытку
    else:
        # Только текстовый ответ
        if is_correct:
            points_awarded = 150
    
    # Создаем запись о попытке
    attempt = UserAttempt.objects.create(
        user=user,
        problem=problem,
        submitted_answer=submitted_answer or 'Фото решения',
        is_correct=is_correct,
        points_awarded=points_awarded,
        time_spent_seconds=time_spent,
        solution_photo=solution_photo,
        ai_analysis=ai_analysis
    )
    
    # Обновляем индекс пользователя
    index_change = user.profile.update_index(
        problem.difficulty_score,
        is_correct
    )
    
    # Формируем ответ
    response_data = {
        'is_correct': is_correct,
        'points_awarded': points_awarded,
        'index_change': index_change,
        'new_index': user.profile.al_khwarizmi_index,
        'correct_answer': problem.correct_answer,
        'solution_steps': problem.solution_steps,
        'attempt_id': attempt.id
    }
    
    if ai_analysis:
        response_data['ai_analysis'] = ai_analysis
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_attempts(request):
    """
    Получение истории попыток пользователя.
    GET /api/problems/attempts/
    """
    user = request.user
    attempts = UserAttempt.objects.filter(user=user).select_related('problem', 'problem__topic')
    
    # Пагинация
    limit = int(request.query_params.get('limit', 20))
    offset = int(request.query_params.get('offset', 0))
    
    total = attempts.count()
    attempts = attempts[offset:offset + limit]
    
    serializer = UserAttemptSerializer(attempts, many=True)
    
    return Response({
        'total': total,
        'results': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def topics_list(request):
    """
    Получение списка всех тем.
    GET /api/problems/topics/
    """
    from .serializers import TopicSerializer
    
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
