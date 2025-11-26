from django.urls import path
from .views import leaderboard, user_arena_stats

urlpatterns = [
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('stats/', user_arena_stats, name='user_arena_stats'),
]
