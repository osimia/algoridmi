import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'al_khwarizmi.settings')
django.setup()

from problems.models import Problem
from django.db.models import Count

# Получаем импортированные задачи для 6 класса
grade6 = Problem.objects.filter(source='imported', grade_level=6)

print(f'✅ Импортировано задач для 6 класса: {grade6.count()}')
print('\n📚 Примеры задач:\n')

for p in grade6[:10]:
    print(f'{p.id}. {p.title}')
    print(f'   Сложность: {p.difficulty_score}')
    print(f'   Тема: {p.topic.name if p.topic else "Не указана"}')
    print(f'   Описание: {p.description[:80]}...')
    if p.correct_answer:
        print(f'   Ответ: {p.correct_answer[:50]}')
    print()

# Статистика по темам
print('\n📊 Статистика по темам для 6 класса:')
topics = Problem.objects.filter(source='imported', grade_level=6).values('topic__name').annotate(count=Count('id')).order_by('-count')
for topic in topics:
    print(f"   - {topic['topic__name']}: {topic['count']} задач")

# Общая статистика по всем классам
print('\n📈 Общая статистика импортированных задач:')
all_grades = Problem.objects.filter(source='imported').values('grade_level').annotate(count=Count('id')).order_by('grade_level')
for grade in all_grades:
    print(f"   - {grade['grade_level']} класс: {grade['count']} задач")
