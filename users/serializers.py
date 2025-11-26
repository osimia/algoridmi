from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Profile"""
    user = UserSerializer(read_only=True)
    division = serializers.ReadOnlyField()
    rank_title = serializers.ReadOnlyField()
    recommended_difficulty = serializers.ReadOnlyField()
    grade_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'user_type', 'age', 'grade', 'school', 'city', 'country',
            'al_khwarizmi_index', 'total_solved_problems', 'total_arena_points',
            'division', 'rank_title', 'recommended_difficulty', 'grade_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'al_khwarizmi_index', 'total_solved_problems',
            'total_arena_points', 'created_at', 'updated_at'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=6
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Подтверждение пароля'
    )
    
    # Поля профиля (опциональные при регистрации)
    user_type = serializers.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES,
        required=False,
        default='student'
    )
    age = serializers.IntegerField(
        required=False,
        min_value=5,
        max_value=100,
        default=15
    )
    grade = serializers.ChoiceField(
        choices=Profile.GRADE_CHOICES,
        required=False,
        allow_null=True
    )
    school = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255
    )
    city = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100
    )
    country = serializers.ChoiceField(
        choices=Profile.COUNTRY_CHOICES,
        required=False,
        default='KZ'
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'user_type', 'age', 'grade', 'school', 'city', 'country'
        ]
    
    def validate(self, attrs):
        """Проверка совпадения паролей"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Пароли не совпадают."
            })
        
        # Устанавливаем значения по умолчанию, если не указаны
        attrs.setdefault('user_type', 'student')
        attrs.setdefault('age', 15)
        attrs.setdefault('country', 'KZ')
        attrs.setdefault('grade', None)
        attrs.setdefault('school', '')
        attrs.setdefault('city', '')
        
        return attrs
    
    def validate_email(self, value):
        """Проверка уникальности email"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value
    
    def create(self, validated_data):
        """Создание пользователя и профиля"""
        # Извлекаем поля профиля с значениями по умолчанию
        profile_data = {
            'country': validated_data.pop('country', 'KZ'),
            'user_type': validated_data.pop('user_type', 'student'),
            'age': validated_data.pop('age', 15),
            'grade': validated_data.pop('grade', None),
            'school': validated_data.pop('school', ''),
            'city': validated_data.pop('city', ''),
        }
        validated_data.pop('password2')
        
        # Создаем пользователя
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Обновляем профиль
        profile = user.profile
        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()
        
        return user


class ProgressSerializer(serializers.Serializer):
    """Сериализатор для отображения прогресса по темам"""
    topic_name = serializers.CharField()
    total_attempts = serializers.IntegerField()
    correct_attempts = serializers.IntegerField()
    success_rate = serializers.FloatField()
    average_difficulty = serializers.FloatField()
