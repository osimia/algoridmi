@echo off
echo ========================================
echo   Импорт Задач для 11 Класса
echo ========================================
echo.
echo Ожидание 2 минут для сброса лимита Gemini API...
echo Пожалуйста, подождите...
echo.
timeout /t 120 /nobreak
echo.
echo ========================================
echo   Начинаем Импорт
echo ========================================
echo.
.\venv\Scripts\python.exe manage.py import_book "c:\Users\Hp\OneDrive\Desktop\algoritm\11.pdf" --topic "Математика: 11 класс" --grade 11 --min-difficulty 1400 --max-difficulty 2200
echo.
echo ========================================
echo   Импорт Завершен
echo ========================================
pause
