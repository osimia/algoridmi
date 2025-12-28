from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Topic(models.Model):
    """
    Категории и темы задач (например, 'Алгебра: Иррациональные уравнения').
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название темы'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    
    difficulty_base = models.IntegerField(
        default=1000,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        verbose_name='Базовая сложность',
        help_text='Средний уровень сложности задач в этой теме'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Problem(models.Model):
    """
    Основная база задач.
    """
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='problems',
        verbose_name='Тема',
        null=True,
        blank=True
    )
    
    title = models.CharField(
        max_length=300,
        verbose_name='Заголовок задачи'
    )
    
    latex_formula = models.TextField(
        verbose_name='Формула (LaTeX)',
        help_text='Математическая формула в формате LaTeX'
    )
    
    description = models.TextField(
        verbose_name='Описание задачи',
        help_text='Текстовое описание задачи'
    )
    
    correct_answer = models.CharField(
        max_length=200,
        verbose_name='Правильный ответ'
    )
    
    difficulty_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        verbose_name='Сложность',
        help_text='Уровень сложности задачи (0-3000)'
    )
    
    solution_steps = models.JSONField(
        default=list,
        verbose_name='Шаги решения',
        help_text='Детальное пошаговое решение в формате JSON'
    )
    
    hints = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Подсказки',
        help_text='Список подсказок для решения'
    )
    
    grade_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        null=True,
        blank=True,
        verbose_name='Класс',
        help_text='Для какого класса предназначена задача (1-12)'
    )
    
    source = models.CharField(
        max_length=50,
        default='ai_generated',
        verbose_name='Источник',
        help_text='Источник задачи (ai_generated, manual, imported)',
        choices=[
            ('ai_generated', 'AI сгенерирована'),
            ('manual', 'Создана вручную'),
            ('imported', 'Импортирована')
        ]
    )
    
    times_used = models.IntegerField(
        default=0,
        verbose_name='Использована раз',
        help_text='Сколько раз задача была показана пользователям'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Доступна ли задача для генерации'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['difficulty_score']),
            models.Index(fields=['grade_level']),
            models.Index(fields=['is_active']),
            models.Index(fields=['source']),
            models.Index(fields=['topic', 'difficulty_score']),
        ]
    
    def __str__(self):
        return f"{self.title} (Сложность: {self.difficulty_score})"


class UserAttempt(models.Model):
    """
    Журнал попыток решения задач пользователями.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Пользователь'
    )
    
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Задача',
        null=True,
        blank=True,
        help_text='Задача из БД (null для AI-генерируемых задач)'
    )
    
    submitted_answer = models.CharField(
        max_length=200,
        verbose_name='Ответ пользователя'
    )
    
    is_correct = models.BooleanField(
        verbose_name='Правильно'
    )
    
    attempt_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата попытки'
    )
    
    points_awarded = models.IntegerField(
        default=0,
        verbose_name='Начислено очков'
    )
    
    time_spent_seconds = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Время решения (сек)'
    )
    
    solution_photo = models.ImageField(
        upload_to='solutions/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name='Фото решения'
    )
    
    ai_analysis = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Анализ ИИ',
        help_text='Результат анализа решения ИИ'
    )
    
    class Meta:
        verbose_name = 'Попытка решения'
        verbose_name_plural = 'Попытки решений'
        ordering = ['-attempt_date']
        indexes = [
            models.Index(fields=['user', '-attempt_date']),
            models.Index(fields=['problem', '-attempt_date']),
            models.Index(fields=['user', 'is_correct']),
            models.Index(fields=['user', 'problem']),
        ]
    
    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        problem_title = self.problem.title if self.problem else "AI-задача"
        return f"{status} {self.user.username} - {problem_title}"
