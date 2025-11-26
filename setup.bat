@echo off
echo ========================================
echo   Установка платформы Ал Хоразми
echo ========================================
echo.

echo [1/6] Создание виртуального окружения...
python -m venv venv
if errorlevel 1 (
    echo Ошибка создания виртуального окружения!
    pause
    exit /b 1
)

echo [2/6] Активация виртуального окружения...
call venv\Scripts\activate.bat

echo [3/6] Установка зависимостей...
pip install -r requirements.txt
if errorlevel 1 (
    echo Ошибка установки зависимостей!
    pause
    exit /b 1
)

echo [4/6] Применение миграций базы данных...
python manage.py migrate
if errorlevel 1 (
    echo Ошибка применения миграций!
    pause
    exit /b 1
)

echo [5/6] Загрузка примеров задач...
python manage.py load_sample_problems

echo [6/6] Создание суперпользователя...
echo.
echo Введите данные для администратора:
python manage.py createsuperuser

echo.
echo ========================================
echo   Установка завершена успешно!
echo ========================================
echo.
echo Для запуска сервера используйте:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Затем откройте браузер: http://localhost:8000
echo Админ-панель: http://localhost:8000/admin
echo.
pause
