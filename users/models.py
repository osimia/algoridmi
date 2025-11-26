from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    """
    Расширенная информация о пользователе.
    Связана с Django User моделью через OneToOne.
    """
    COUNTRY_CHOICES = [
        ('RU', 'Россия'),
        ('KZ', 'Казахстан'),
        ('UZ', 'Узбекистан'),
        ('KG', 'Кыргызстан'),
        ('TJ', 'Таджикистан'),
        ('UA', 'Украина'),
        ('BY', 'Беларусь'),
        ('AZ', 'Азербайджан'),
        ('OTHER', 'Другая'),
    ]
    
    USER_TYPE_CHOICES = [
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
        ('university', 'Студент'),
        ('other', 'Другое'),
    ]
    
    GRADE_CHOICES = [
        (1, '1 класс'),
        (2, '2 класс'),
        (3, '3 класс'),
        (4, '4 класс'),
        (5, '5 класс'),
        (6, '6 класс'),
        (7, '7 класс'),
        (8, '8 класс'),
        (9, '9 класс'),
        (10, '10 класс'),
        (11, '11 класс'),
        (12, '12 класс / Выпускник'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='student',
        verbose_name='Тип пользователя'
    )
    
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Возраст'
    )
    
    grade = models.PositiveIntegerField(
        null=True,
        blank=True,
        choices=GRADE_CHOICES,
        verbose_name='Класс'
    )
    
    school = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Школа/Университет'
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Город'
    )
    
    country = models.CharField(
        max_length=10,
        choices=COUNTRY_CHOICES,
        default='KZ',
        verbose_name='Страна'
    )
    
    al_khwarizmi_index = models.IntegerField(
        default=1000,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        verbose_name='Индекс Ал Хоразми',
        help_text='Рейтинг пользователя (0-3000)'
    )
    
    total_solved_problems = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Всего решено задач'
    )
    
    total_arena_points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Всего очков арены'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-al_khwarizmi_index']
    
    def __str__(self):
        return f"{self.user.username} - Индекс: {self.al_khwarizmi_index}"
    
    @property
    def division(self):
        """Определяет дивизион пользователя на основе индекса"""
        if self.al_khwarizmi_index < 500:
            return 'Лига Новичков'
        elif self.al_khwarizmi_index < 1550:
            return 'Лига Евклида'
        else:
            return 'Лига Эйнштейна'
    
    @property
    def rank_title(self):
        """Определяет звание пользователя"""
        if self.al_khwarizmi_index < 500:
            return 'Новичок'
        elif self.al_khwarizmi_index < 1000:
            return 'Ученик'
        elif self.al_khwarizmi_index < 1500:
            return 'Адепт'
        elif self.al_khwarizmi_index < 2000:
            return 'Магистр'
        else:
            return 'Гроссмейстер'
    
    @property
    def recommended_difficulty(self):
        """Рекомендуемая сложность задач на основе класса и возраста"""
        # Если указан класс, используем его
        if self.grade:
            grade_difficulty_map = {
                1: 200,   # 1 класс - базовая арифметика
                2: 300,   # 2 класс
                3: 400,   # 3 класс
                4: 500,   # 4 класс
                5: 700,   # 5 класс - начало алгебры
                6: 900,   # 6 класс
                7: 1100,  # 7 класс - геометрия
                8: 1300,  # 8 класс
                9: 1500,  # 9 класс - подготовка к ОГЭ
                10: 1700, # 10 класс
                11: 1900, # 11 класс - подготовка к ЕГЭ
                12: 2100, # Выпускник/Олимпиады
            }
            base_difficulty = grade_difficulty_map.get(self.grade, 1000)
        # Если класс не указан, используем возраст
        elif self.age:
            if self.age <= 7:
                base_difficulty = 200
            elif self.age <= 10:
                base_difficulty = 400
            elif self.age <= 13:
                base_difficulty = 800
            elif self.age <= 15:
                base_difficulty = 1200
            elif self.age <= 17:
                base_difficulty = 1600
            else:
                base_difficulty = 1800
        else:
            # По умолчанию используем текущий индекс
            base_difficulty = self.al_khwarizmi_index
        
        # Корректируем на основе текущего индекса (±200)
        return max(200, min(2500, (base_difficulty + self.al_khwarizmi_index) // 2))
    
    @property
    def grade_display(self):
        """Отображение класса или типа пользователя"""
        if self.user_type == 'teacher':
            return 'Учитель'
        elif self.user_type == 'university':
            return 'Студент'
        elif self.grade:
            return f'{self.grade} класс'
        elif self.age:
            return f'{self.age} лет'
        return 'Не указано'
    
    @property
    def is_profile_complete(self):
        """Проверка заполненности профиля"""
        # Обязательные поля: user_type, age, country
        if not self.user_type or not self.age or not self.country:
            return False
        
        # Для студентов обязателен класс
        if self.user_type == 'student' and not self.grade:
            return False
        
        return True
    
    def update_index(self, problem_difficulty, is_correct):
        """
        Обновляет индекс пользователя по ELO-подобному алгоритму.
        
        Args:
            problem_difficulty: Сложность задачи (difficulty_score)
            is_correct: Правильно ли решена задача
        """
        K = 32  # Коэффициент изменения рейтинга
        
        # Ожидаемая вероятность успеха
        expected = 1 / (1 + 10 ** ((problem_difficulty - self.al_khwarizmi_index) / 400))
        
        # Фактический результат (1 - успех, 0 - неудача)
        actual = 1 if is_correct else 0
        
        # Изменение рейтинга
        delta = K * (actual - expected)
        
        # Обновляем индекс
        new_index = self.al_khwarizmi_index + int(delta)
        self.al_khwarizmi_index = max(0, min(3000, new_index))
        
        if is_correct:
            self.total_solved_problems += 1
        
        self.save()
        
        return int(delta)
