from django.urls import path
from .views import (
    generate_problem, submit_answer,
    user_attempts, topics_list
)
from .views_gemini import (
    generate_problem_ai, submit_answer_ai,
    available_topics
)
from .views_book_import import (
    upload_and_import_book, import_from_text,
    import_statistics
)

urlpatterns = [
    # Оригинальные endpoints (статические задачи из БД)
    path('generate/', generate_problem, name='generate_problem'),
    path('submit/', submit_answer, name='submit_answer'),
    path('attempts/', user_attempts, name='user_attempts'),
    path('topics/', topics_list, name='topics_list'),
    
    # Новые endpoints с Gemini AI
    path('generate-ai/', generate_problem_ai, name='generate_problem_ai'),
    path('submit-ai/', submit_answer_ai, name='submit_answer_ai'),
    path('topics-ai/', available_topics, name='available_topics'),
    
    # Импорт задач из книг (только для админов)
    path('import/book/', upload_and_import_book, name='upload_import_book'),
    path('import/text/', import_from_text, name='import_from_text'),
    path('import/statistics/', import_statistics, name='import_statistics'),
]
