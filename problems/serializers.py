from rest_framework import serializers
from .models import Topic, Problem, UserAttempt


class TopicSerializer(serializers.ModelSerializer):
    """Сериализатор для темы задач"""
    
    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'difficulty_base', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProblemSerializer(serializers.ModelSerializer):
    """Сериализатор для задачи"""
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    
    class Meta:
        model = Problem
        fields = [
            'id', 'topic', 'topic_name', 'title', 'latex_formula',
            'description', 'difficulty_score', 'hints', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProblemDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для задачи (включая решение)"""
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    
    class Meta:
        model = Problem
        fields = [
            'id', 'topic', 'topic_name', 'title', 'latex_formula',
            'description', 'correct_answer', 'difficulty_score',
            'solution_steps', 'hints', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserAttemptSerializer(serializers.ModelSerializer):
    """Сериализатор для попытки решения"""
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserAttempt
        fields = [
            'id', 'user', 'user_name', 'problem', 'problem_title',
            'submitted_answer', 'is_correct', 'attempt_date',
            'points_awarded', 'time_spent_seconds', 'solution_photo'
        ]
        read_only_fields = [
            'id', 'user', 'is_correct', 'attempt_date', 'points_awarded'
        ]


class SubmitAnswerSerializer(serializers.Serializer):
    """Сериализатор для отправки ответа на задачу"""
    problem_id = serializers.IntegerField(required=True)
    submitted_answer = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=200
    )
    solution_photo = serializers.ImageField(
        required=False,
        allow_null=True
    )
    time_spent_seconds = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=0
    )
    
    def validate(self, attrs):
        """Проверка, что предоставлен либо ответ, либо фото"""
        submitted_answer = attrs.get('submitted_answer', '')
        solution_photo = attrs.get('solution_photo')
        
        if not submitted_answer and not solution_photo:
            raise serializers.ValidationError(
                "Необходимо предоставить либо ответ, либо фото решения"
            )
        
        return attrs
