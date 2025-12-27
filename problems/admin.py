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
        'title', 'topic', 'difficulty_score', 'grade_level', 
        'source', 'times_used', 'is_active', 'created_at'
    ]
    list_filter = [
        'topic', 'difficulty_score', 'grade_level', 
        'source', 'is_active', 'created_at'
    ]
    search_fields = ['title', 'description', 'latex_formula']
    readonly_fields = ['created_at', 'updated_at', 'times_used']
    actions = ['activate_problems', 'deactivate_problems', 'reset_usage_counter']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('topic', 'title', 'difficulty_score', 'grade_level', 'source', 'is_active')
        }),
        ('Содержание задачи', {
            'fields': ('latex_formula', 'description', 'correct_answer')
        }),
        ('Решение и подсказки', {
            'fields': ('solution_steps', 'hints')
        }),
        ('Статистика', {
            'fields': ('times_used',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def activate_problems(self, request, queryset):
        """Активировать выбранные задачи"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано задач: {updated}')
    activate_problems.short_description = "✅ Активировать выбранные задачи"
    
    def deactivate_problems(self, request, queryset):
        """Деактивировать выбранные задачи"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано задач: {updated}')
    deactivate_problems.short_description = "❌ Деактивировать выбранные задачи"
    
    def reset_usage_counter(self, request, queryset):
        """Сбросить счетчик использования"""
        updated = queryset.update(times_used=0)
        self.message_user(request, f'Сброшен счетчик для {updated} задач')
    reset_usage_counter.short_description = "🔄 Сбросить счетчик использования"


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
