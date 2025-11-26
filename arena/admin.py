from django.contrib import admin
from .models import ArenaRank


@admin.register(ArenaRank)
class ArenaRankAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'current_division', 'rank', 'current_index',
        'weekly_score', 'total_cups', 'total_medals', 'last_updated'
    ]
    list_filter = ['current_division', 'last_updated']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_updated']
    
    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Рейтинг', {
            'fields': ('current_index', 'current_division', 'rank', 'weekly_score')
        }),
        ('Достижения', {
            'fields': ('total_cups', 'total_medals')
        }),
        ('Информация', {
            'fields': ('last_updated',)
        }),
    )
