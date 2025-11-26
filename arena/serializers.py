from rest_framework import serializers
from .models import ArenaRank


class ArenaRankSerializer(serializers.ModelSerializer):
    """Сериализатор для рейтинга арены"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    division_display = serializers.CharField(source='get_current_division_display', read_only=True)
    
    class Meta:
        model = ArenaRank
        fields = [
            'id', 'user', 'username', 'email', 'current_index',
            'current_division', 'division_display', 'weekly_score',
            'rank', 'total_cups', 'total_medals', 'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']
