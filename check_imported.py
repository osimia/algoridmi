import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'al_khwarizmi.settings')
django.setup()

from problems.models import Problem

# Получаем импортированные задачи для 5 класса
imported = Problem.objects.filter(source='imported', grade_level=5)

print(f'✅ Импортировано задач для 5 класса: {imported.count()}')
print('\n📚 Примеры задач:\n')

for p in imported[:10]:
    print(f'{p.id}. {p.title}')
    print(f'   Сложность: {p.difficulty_score}')
    print(f'   Тема: {p.topic.name if p.topic else "Не указана"}')
    print(f'   Описание: {p.description[:100]}...')
    print(f'   Ответ: {p.correct_answer}')
    print()

# Статистика по темам
print('\n📊 Статистика по темам:')
from django.db.models import Count
topics = Problem.objects.filter(source='imported', grade_level=5).values('topic__name').annotate(count=Count('id'))
for topic in topics:
    print(f"   - {topic['topic__name']}: {topic['count']} задач")
