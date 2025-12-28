from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Q, Avg
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .models import Profile
from .serializers import (
    RegisterSerializer, UserSerializer, ProfileSerializer, ProgressSerializer
)
from problems.models import UserAttempt, Topic


@api_view(['GET'])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Получение CSRF токена для frontend.
    GET /api/auth/csrf/
    """
    return Response({'detail': 'CSRF cookie set'})


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Регистрация нового пользователя.
    POST /api/auth/register/
    """
    # Логирование для отладки
    print("Received data:", request.data)
    
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Автоматический вход после регистрации
        login(request, user)
        
        return Response({
            'message': 'Регистрация успешна',
            'user': UserSerializer(user).data,
            'profile': ProfileSerializer(user.profile).data,
        }, status=status.HTTP_201_CREATED)
    
    # Логирование ошибок
    print("Validation errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Вход пользователя.
    POST /api/auth/login/
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'error': 'Требуются email и пароль'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Находим пользователя по email
    try:
        from django.contrib.auth.models import User
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({
                'error': 'Неверные учетные данные'
            }, status=status.HTTP_401_UNAUTHORIZED)
        username = user.username
    except Exception as e:
        return Response({
            'error': 'Ошибка входа'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Аутентификация
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Вход через сессию
        login(request, user)
        
        return Response({
            'message': 'Вход выполнен успешно',
            'user': UserSerializer(user).data,
            'profile': ProfileSerializer(user.profile).data,
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Неверные учетные данные'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Выход пользователя через сессию.
    POST /api/auth/logout/
    """
    logout(request)
    return Response({
        'message': 'Выход выполнен успешно'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Получение информации о текущем пользователе (для проверки сессии).
    GET /api/user/profile/
    """
    user = request.user
    
    # Возвращаем структуру, совместимую с login/register
    return Response({
        'user': UserSerializer(user).data,
        'profile': ProfileSerializer(user.profile).data,
    }, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Получение и обновление профиля текущего пользователя.
    GET/PUT /api/user/profile-detail/
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def progress_view(request):
    """
    Получение прогресса пользователя по темам.
    GET /api/user/progress/
    Включает статистику по обычным задачам и AI-генерируемым задачам.
    ОПТИМИЗИРОВАНО: использует агрегацию вместо циклов.
    """
    user = request.user
    
    # ОПТИМИЗАЦИЯ: Получаем статистику одним запросом с агрегацией
    from django.db.models import Case, When, FloatField
    
    topics_stats = Topic.objects.annotate(
        total_attempts=Count(
            'problem__userattempt',
            filter=Q(problem__userattempt__user=user)
        ),
        correct_attempts=Count(
            'problem__userattempt',
            filter=Q(problem__userattempt__user=user, problem__userattempt__is_correct=True)
        ),
        avg_difficulty=Avg(
            'problem__difficulty_score',
            filter=Q(problem__userattempt__user=user)
        )
    ).filter(total_attempts__gt=0)
    
    progress_data = []
    
    for topic in topics_stats:
        success_rate = (topic.correct_attempts / topic.total_attempts * 100) if topic.total_attempts > 0 else 0
        
        progress_data.append({
            'topic_name': topic.name,
            'total_attempts': topic.total_attempts,
            'correct_attempts': topic.correct_attempts,
            'success_rate': round(success_rate, 1),
            'average_difficulty': round(topic.avg_difficulty or 0, 1)
        })
    
    # Добавляем статистику по AI-генерируемым задачам (где problem=None)
    ai_attempts = UserAttempt.objects.filter(
        user=user,
        problem__isnull=True  # AI-задачи не имеют problem
    )
    
    ai_total = ai_attempts.count()
    if ai_total > 0:
        ai_correct = ai_attempts.filter(is_correct=True).count()
        ai_success_rate = (ai_correct / ai_total) * 100
        
        # Извлекаем сложность из ai_analysis JSON поля
        from django.db.models import JSONField
        total_difficulty = 0
        count_with_difficulty = 0
        
        for attempt in ai_attempts:
            if attempt.ai_analysis and 'problem_data' in attempt.ai_analysis:
                difficulty = attempt.ai_analysis['problem_data'].get('difficulty', 0)
                if difficulty:
                    total_difficulty += difficulty
                    count_with_difficulty += 1
        
        avg_ai_difficulty = total_difficulty / count_with_difficulty if count_with_difficulty > 0 else 0
        
        progress_data.append({
            'topic_name': 'AI-генерируемые задачи',
            'total_attempts': ai_total,
            'correct_attempts': ai_correct,
            'success_rate': round(ai_success_rate, 1),
            'average_difficulty': round(avg_ai_difficulty, 1)
        })
    
    serializer = ProgressSerializer(progress_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
