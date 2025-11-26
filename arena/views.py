from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ArenaRank
from .serializers import ArenaRankSerializer


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
    user = request.user
    division = request.query_params.get('division')
    limit = int(request.query_params.get('limit', 10))
    
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
    
    # Получаем топ игроков дивизиона
    leaderboard_query = ArenaRank.objects.filter(
        current_division=division
    ).select_related('user').order_by('rank', '-weekly_score')[:limit]
    
    # Получаем информацию о текущем пользователе
    user_rank = None
    if hasattr(user, 'arena_rank'):
        user_rank = ArenaRankSerializer(user.arena_rank).data
    
    # Сериализуем данные
    serializer = ArenaRankSerializer(leaderboard_query, many=True)
    
    return Response({
        'division': division,
        'leaderboard': serializer.data,
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
