from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ArenaRank
from .serializers import ArenaRankSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    """
    Получение таблицы лидеров арены.
    GET /api/arena/leaderboard/
    
    Параметры:
    - division: Дивизион (NOVICE, EUCLID, EINSTEIN) - опционально
    - limit: Количество записей (по умолчанию 10)
    """
    try:
        user = request.user
        logger.info(f"Leaderboard request from user: {user.username}, authenticated: {user.is_authenticated}")
        
        division = request.query_params.get('division')
        limit = int(request.query_params.get('limit', 10))
        
        # Проверяем наличие профиля
        if not hasattr(user, 'profile'):
            logger.error(f"User {user.username} has no profile")
            return Response({
                'error': 'Профиль пользователя не найден',
                'message': 'Пожалуйста, заполните профиль'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Если дивизион не указан, используем дивизион текущего пользователя
        if not division:
            if hasattr(user, 'arena_rank'):
                division = user.arena_rank.current_division
            else:
                # Создаем запись в арене для пользователя, если её нет
                arena_rank, created = ArenaRank.objects.get_or_create(
                    user=user,
                    defaults={
                        'current_index': user.profile.al_khwarizmi_index,
                        'current_division': ArenaRank.get_division_from_index(
                            user.profile.al_khwarizmi_index
                        )
                    }
                )
                division = arena_rank.current_division
    except Exception as e:
        logger.exception(f"Error in leaderboard view: {str(e)}")
        return Response({
            'error': 'Ошибка при получении рейтинга',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Получаем топ игроков дивизиона (сортировка по очкам, затем по индексу)
    leaderboard_query = ArenaRank.objects.filter(
        current_division=division
    ).select_related('user').order_by('-weekly_score', '-current_index')[:limit]
    
    # Получаем информацию о текущем пользователе
    user_rank = None
    if hasattr(user, 'arena_rank'):
        user_rank = ArenaRankSerializer(user.arena_rank).data
    
    # Сериализуем данные и добавляем правильные места
    serializer = ArenaRankSerializer(leaderboard_query, many=True)
    leaderboard_data = serializer.data
    
    # Присваиваем правильные места (1, 2, 3, 4...)
    for position, player in enumerate(leaderboard_data, start=1):
        player['rank'] = position
    
    return Response({
        'division': division,
        'leaderboard': leaderboard_data,
        'user_rank': user_rank
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_arena_stats(request):
    """
    Получение статистики пользователя в арене.
    GET /api/arena/stats/
    """
    user = request.user
    
    # Получаем или создаем запись в арене
    arena_rank, created = ArenaRank.objects.get_or_create(
        user=user,
        defaults={
            'current_index': user.profile.al_khwarizmi_index,
            'current_division': ArenaRank.get_division_from_index(
                user.profile.al_khwarizmi_index
            )
        }
    )
    
    if not created:
        # Обновляем данные из профиля
        arena_rank.update_from_profile()
    
    serializer = ArenaRankSerializer(arena_rank)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
