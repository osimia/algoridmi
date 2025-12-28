@echo off
echo Импорт задач для 8 класса...
.\venv\Scripts\python.exe manage.py import_book "c:\Users\Hp\OneDrive\Desktop\algoritm\8 класс Матем рус.pdf" --topic "Математика: 8 класс" --grade 8 --min-difficulty 900 --max-difficulty 1600
pause
