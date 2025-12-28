@echo off
echo Ожидание 20 секунд для сброса лимита API...
timeout /t 20 /nobreak
echo.
echo Импорт задач для 11 класса...
.\venv\Scripts\python.exe manage.py import_book "c:\Users\Hp\OneDrive\Desktop\algoritm\11.pdf" --topic "Математика: 11 класс" --grade 11 --min-difficulty 1400 --max-difficulty 2200
pause
