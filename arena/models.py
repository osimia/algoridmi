from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class ArenaRank(models.Model):
    """
    Рейтинговая таблица для Арены.
    Обновляется периодически (еженедельно) через management command.
    """
    DIVISION_CHOICES = [
        ('NOVICE', 'Лига Новичков'),
        ('EUCLID', 'Лига Евклида'),
        ('EINSTEIN', 'Лига Эйнштейна'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='arena_rank',
        verbose_name='Пользователь'
    )
    
    current_index = models.IntegerField(
        default=1000,
        verbose_name='Текущий индекс',
        help_text='Копия индекса из профиля для быстрого доступа'
    )
    
    current_division = models.CharField(
        max_length=20,
        choices=DIVISION_CHOICES,
        default='EUCLID',
        verbose_name='Текущий дивизион'
    )
    
    weekly_score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Очки за неделю',
        help_text='Очки, заработанные за текущую неделю'
    )
    
    rank = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Место в рейтинге',
        help_text='Место в текущем дивизионе'
    )
    
    total_cups = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Всего кубков',
        help_text='Количество выигранных дивизионных кубков'
    )
    
    total_medals = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Всего медалей',
        help_text='Количество золотых медалей (топ-3)'
    )
    
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Последнее обновление'
    )
    
    class Meta:
        verbose_name = 'Рейтинг арены'
        verbose_name_plural = 'Рейтинги арены'
        ordering = ['current_division', 'rank']
        indexes = [
            models.Index(fields=['current_division', 'rank']),
            models.Index(fields=['current_division', '-weekly_score']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_current_division_display()} (#{self.rank})"
    
    @staticmethod
    def get_division_from_index(index):
        """Определяет дивизион на основе индекса"""
        if index < 500:
            return 'NOVICE'
        elif index < 1550:
            return 'EUCLID'
        else:
            return 'EINSTEIN'
    
    def update_from_profile(self):
        """Обновляет данные из профиля пользователя"""
        profile = self.user.profile
        self.current_index = profile.al_khwarizmi_index
        self.current_division = self.get_division_from_index(self.current_index)
        self.save()
    
    def update_rank(self):
        """Обновляет место в рейтинге на основе weekly_score"""
        # Считаем количество пользователей в том же дивизионе с большим weekly_score
        better_count = ArenaRank.objects.filter(
            current_division=self.current_division,
            weekly_score__gt=self.weekly_score
        ).count()
        self.rank = better_count + 1
        self.save(update_fields=['rank'])
