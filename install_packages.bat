@echo off
echo ========================================
echo Установка зависимостей для Al Khwarizmi
echo ========================================
echo.

REM Активация виртуального окружения
call venv\Scripts\activate

echo [1/9] Установка Django...
pip install Django==4.2.7
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить Django
    pause
    exit /b 1
)

echo [2/9] Установка Django REST Framework...
pip install djangorestframework==3.14.0
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить DRF
    pause
    exit /b 1
)

echo [3/9] Установка JWT...
pip install djangorestframework-simplejwt==5.3.0
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить JWT
    pause
    exit /b 1
)

echo [4/9] Установка PostgreSQL драйвера...
pip install psycopg2-binary==2.9.9
if %errorlevel% neq 0 (
    echo ПРЕДУПРЕЖДЕНИЕ: Не удалось установить psycopg2-binary
    echo Это нормально, если вы используете SQLite
)

echo [5/9] Установка CORS headers...
pip install django-cors-headers==4.3.1
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить CORS headers
    pause
    exit /b 1
)

echo [6/9] Установка python-decouple...
pip install python-decouple==3.8
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить python-decouple
    pause
    exit /b 1
)

echo [7/9] Установка Pillow (может занять время)...
pip install Pillow
if %errorlevel% neq 0 (
    echo ПРЕДУПРЕЖДЕНИЕ: Не удалось установить Pillow
    echo Функция загрузки фото решений будет недоступна
)

echo [8/9] Установка Google Gemini AI...
pip install google-genai==1.0.0
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить google-genai
    pause
    exit /b 1
)

echo [9/9] Установка django-extensions...
pip install django-extensions==3.2.3
if %errorlevel% neq 0 (
    echo ПРЕДУПРЕЖДЕНИЕ: Не удалось установить django-extensions
    echo Это опциональный пакет
)

echo.
echo ========================================
echo ✅ Установка завершена!
echo ========================================
echo.
echo Следующие шаги:
echo 1. Добавьте GEMINI_API_KEY в .env файл
echo 2. Добавьте DATABASE_PUBLIC_URL в .env файл (если используете Railway)
echo 3. Запустите: python manage.py migrate
echo 4. Запустите: python manage.py createsuperuser
echo 5. Запустите: python manage.py runserver
echo.
pause
