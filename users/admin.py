from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'country', 'al_khwarizmi_index',
        'total_solved_problems', 'division', 'rank_title', 'created_at'
    ]
    list_filter = ['country', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'division', 'rank_title']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'country')
        }),
        ('Статистика', {
            'fields': (
                'al_khwarizmi_index', 'total_solved_problems',
                'total_arena_points', 'division', 'rank_title'
            )
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )
