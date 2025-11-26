from django.contrib import admin
from .models import Topic, Problem, UserAttempt


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty_base', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['difficulty_base', 'created_at']


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'topic', 'difficulty_score', 'is_active', 'created_at'
    ]
    list_filter = ['topic', 'difficulty_score', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'latex_formula']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('topic', 'title', 'difficulty_score', 'is_active')
        }),
        ('Содержание задачи', {
            'fields': ('latex_formula', 'description', 'correct_answer')
        }),
        ('Решение и подсказки', {
            'fields': ('solution_steps', 'hints')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(UserAttempt)
class UserAttemptAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'problem', 'is_correct', 'points_awarded',
        'attempt_date'
    ]
    list_filter = ['is_correct', 'attempt_date', 'problem__topic']
    search_fields = ['user__username', 'problem__title']
    readonly_fields = ['attempt_date']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'problem', 'submitted_answer')
        }),
        ('Результат', {
            'fields': ('is_correct', 'points_awarded', 'time_spent_seconds')
        }),
        ('Дополнительно', {
            'fields': ('solution_photo', 'ai_analysis', 'attempt_date')
        }),
    )
