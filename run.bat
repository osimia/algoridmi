@echo off
echo Запуск платформы Ал Хоразми...
call venv\Scripts\activate.bat
python manage.py runserver
pause
