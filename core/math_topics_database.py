"""
База данных математических тем для всех уровней
От 1 класса до профессионального уровня
Всего: 1000+ тем
"""

# Структура: {
#   'topic': 'Название темы',
#   'grade_min': минимальный класс,
#   'grade_max': максимальный класс,
#   'difficulty_min': минимальная сложность (0-3000),
#   'difficulty_max': максимальная сложность,
#   'category': 'Категория'
# }

MATH_TOPICS_DATABASE = [
    
    # ==================== 1 КЛАСС (6-7 лет) ====================
    # Сложность: 0-200
    
    # Счет и числа
    {"topic": "Счет от 1 до 10", "grade_min": 1, "grade_max": 1, "difficulty_min": 0, "difficulty_max": 50, "category": "Арифметика"},
    {"topic": "Счет от 1 до 20", "grade_min": 1, "grade_max": 1, "difficulty_min": 50, "difficulty_max": 100, "category": "Арифметика"},
    {"topic": "Сравнение чисел до 10", "grade_min": 1, "grade_max": 1, "difficulty_min": 50, "difficulty_max": 100, "category": "Арифметика"},
    {"topic": "Сравнение чисел до 20", "grade_min": 1, "grade_max": 2, "difficulty_min": 100, "difficulty_max": 150, "category": "Арифметика"},
    
    # Сложение и вычитание
    {"topic": "Сложение в пределах 10", "grade_min": 1, "grade_max": 1, "difficulty_min": 50, "difficulty_max": 100, "category": "Арифметика"},
    {"topic": "Вычитание в пределах 10", "grade_min": 1, "grade_max": 1, "difficulty_min": 50, "difficulty_max": 100, "category": "Арифметика"},
    {"topic": "Сложение и вычитание в пределах 10", "grade_min": 1, "grade_max": 1, "difficulty_min": 75, "difficulty_max": 125, "category": "Арифметика"},
    {"topic": "Сложение с переходом через десяток", "grade_min": 1, "grade_max": 2, "difficulty_min": 100, "difficulty_max": 150, "category": "Арифметика"},
    {"topic": "Вычитание с переходом через десяток", "grade_min": 1, "grade_max": 2, "difficulty_min": 100, "difficulty_max": 150, "category": "Арифметика"},
    {"topic": "Сложение в пределах 20", "grade_min": 1, "grade_max": 2, "difficulty_min": 100, "difficulty_max": 150, "category": "Арифметика"},
    {"topic": "Вычитание в пределах 20", "grade_min": 1, "grade_max": 2, "difficulty_min": 100, "difficulty_max": 150, "category": "Арифметика"},
    
    # Геометрия базовая
    {"topic": "Распознавание геометрических фигур", "grade_min": 1, "grade_max": 2, "difficulty_min": 50, "difficulty_max": 100, "category": "Геометрия"},
    {"topic": "Сравнение размеров предметов", "grade_min": 1, "grade_max": 1, "difficulty_min": 25, "difficulty_max": 75, "category": "Геометрия"},
    
    # Текстовые задачи
    {"topic": "Простые задачи на сложение", "grade_min": 1, "grade_max": 2, "difficulty_min": 75, "difficulty_max": 125, "category": "Текстовые задачи"},
    {"topic": "Простые задачи на вычитание", "grade_min": 1, "grade_max": 2, "difficulty_min": 75, "difficulty_max": 125, "category": "Текстовые задачи"},
    
    # ==================== 2 КЛАСС (7-8 лет) ====================
    # Сложность: 100-300
    
    {"topic": "Счет до 100", "grade_min": 2, "grade_max": 2, "difficulty_min": 100, "difficulty_max": 150, "category": "Арифметика"},
    {"topic": "Сложение двузначных чисел без перехода", "grade_min": 2, "grade_max": 2, "difficulty_min": 150, "difficulty_max": 200, "category": "Арифметика"},
    {"topic": "Сложение двузначных чисел с переходом", "grade_min": 2, "grade_max": 3, "difficulty_min": 200, "difficulty_max": 250, "category": "Арифметика"},
    {"topic": "Вычитание двузначных чисел без перехода", "grade_min": 2, "grade_max": 2, "difficulty_min": 150, "difficulty_max": 200, "category": "Арифметика"},
    {"topic": "Вычитание двузначных чисел с переходом", "grade_min": 2, "grade_max": 3, "difficulty_min": 200, "difficulty_max": 250, "category": "Арифметика"},
    {"topic": "Умножение на 2", "grade_min": 2, "grade_max": 2, "difficulty_min": 150, "difficulty_max": 200, "category": "Арифметика"},
    {"topic": "Умножение на 3", "grade_min": 2, "grade_max": 2, "difficulty_min": 150, "difficulty_max": 200, "category": "Арифметика"},
    {"topic": "Деление на 2", "grade_min": 2, "grade_max": 3, "difficulty_min": 175, "difficulty_max": 225, "category": "Арифметика"},
    {"topic": "Деление на 3", "grade_min": 2, "grade_max": 3, "difficulty_min": 175, "difficulty_max": 225, "category": "Арифметика"},
    {"topic": "Периметр прямоугольника", "grade_min": 2, "grade_max": 3, "difficulty_min": 200, "difficulty_max": 250, "category": "Геометрия"},
    {"topic": "Задачи на нахождение суммы", "grade_min": 2, "grade_max": 3, "difficulty_min": 150, "difficulty_max": 200, "category": "Текстовые задачи"},
    {"topic": "Задачи на нахождение остатка", "grade_min": 2, "grade_max": 3, "difficulty_min": 150, "difficulty_max": 200, "category": "Текстовые задачи"},
    
    # ==================== 3 КЛАСС (8-9 лет) ====================
    # Сложность: 200-400
    
    {"topic": "Таблица умножения на 4", "grade_min": 3, "grade_max": 3, "difficulty_min": 200, "difficulty_max": 250, "category": "Арифметика"},
    {"topic": "Таблица умножения на 5", "grade_min": 3, "grade_max": 3, "difficulty_min": 200, "difficulty_max": 250, "category": "Арифметика"},
    {"topic": "Таблица умножения на 6", "grade_min": 3, "grade_max": 3, "difficulty_min": 225, "difficulty_max": 275, "category": "Арифметика"},
    {"topic": "Таблица умножения на 7", "grade_min": 3, "grade_max": 3, "difficulty_min": 225, "difficulty_max": 275, "category": "Арифметика"},
    {"topic": "Таблица умножения на 8", "grade_min": 3, "grade_max": 3, "difficulty_min": 250, "difficulty_max": 300, "category": "Арифметика"},
    {"topic": "Таблица умножения на 9", "grade_min": 3, "grade_max": 3, "difficulty_min": 250, "difficulty_max": 300, "category": "Арифметика"},
    {"topic": "Деление с остатком", "grade_min": 3, "grade_max": 4, "difficulty_min": 275, "difficulty_max": 325, "category": "Арифметика"},
    {"topic": "Трехзначные числа: сложение", "grade_min": 3, "grade_max": 4, "difficulty_min": 250, "difficulty_max": 300, "category": "Арифметика"},
    {"topic": "Трехзначные числа: вычитание", "grade_min": 3, "grade_max": 4, "difficulty_min": 250, "difficulty_max": 300, "category": "Арифметика"},
    {"topic": "Умножение двузначного на однозначное", "grade_min": 3, "grade_max": 4, "difficulty_min": 300, "difficulty_max": 350, "category": "Арифметика"},
    {"topic": "Площадь прямоугольника", "grade_min": 3, "grade_max": 4, "difficulty_min": 275, "difficulty_max": 325, "category": "Геометрия"},
    {"topic": "Площадь квадрата", "grade_min": 3, "grade_max": 4, "difficulty_min": 250, "difficulty_max": 300, "category": "Геометрия"},
    {"topic": "Задачи на умножение", "grade_min": 3, "grade_max": 4, "difficulty_min": 250, "difficulty_max": 300, "category": "Текстовые задачи"},
    {"topic": "Задачи на деление", "grade_min": 3, "grade_max": 4, "difficulty_min": 250, "difficulty_max": 300, "category": "Текстовые задачи"},
    
    # ==================== 4 КЛАСС (9-10 лет) ====================
    # Сложность: 300-500
    
    {"topic": "Многозначные числа: сложение", "grade_min": 4, "grade_max": 5, "difficulty_min": 300, "difficulty_max": 400, "category": "Арифметика"},
    {"topic": "Многозначные числа: вычитание", "grade_min": 4, "grade_max": 5, "difficulty_min": 300, "difficulty_max": 400, "category": "Арифметика"},
    {"topic": "Умножение на двузначное число", "grade_min": 4, "grade_max": 5, "difficulty_min": 350, "difficulty_max": 450, "category": "Арифметика"},
    {"topic": "Деление на двузначное число", "grade_min": 4, "grade_max": 5, "difficulty_min": 400, "difficulty_max": 500, "category": "Арифметика"},
    {"topic": "Порядок действий в выражениях", "grade_min": 4, "grade_max": 5, "difficulty_min": 350, "difficulty_max": 450, "category": "Арифметика"},
    {"topic": "Скобки в выражениях", "grade_min": 4, "grade_max": 5, "difficulty_min": 375, "difficulty_max": 475, "category": "Арифметика"},
    {"topic": "Единицы измерения длины", "grade_min": 4, "grade_max": 5, "difficulty_min": 300, "difficulty_max": 400, "category": "Величины"},
    {"topic": "Единицы измерения массы", "grade_min": 4, "grade_max": 5, "difficulty_min": 300, "difficulty_max": 400, "category": "Величины"},
    {"topic": "Единицы измерения времени", "grade_min": 4, "grade_max": 5, "difficulty_min": 325, "difficulty_max": 425, "category": "Величины"},
    {"topic": "Периметр сложных фигур", "grade_min": 4, "grade_max": 5, "difficulty_min": 350, "difficulty_max": 450, "category": "Геометрия"},
    {"topic": "Площадь сложных фигур", "grade_min": 4, "grade_max": 5, "difficulty_min": 375, "difficulty_max": 475, "category": "Геометрия"},
    {"topic": "Задачи на движение (простые)", "grade_min": 4, "grade_max": 5, "difficulty_min": 400, "difficulty_max": 500, "category": "Текстовые задачи"},
    {"topic": "Задачи на работу (простые)", "grade_min": 4, "grade_max": 5, "difficulty_min": 425, "difficulty_max": 525, "category": "Текстовые задачи"},
    
    # ==================== 5 КЛАСС (10-11 лет) ====================
    # Сложность: 400-700
    
    {"topic": "Натуральные числа и нуль", "grade_min": 5, "grade_max": 5, "difficulty_min": 400, "difficulty_max": 500, "category": "Арифметика"},
    {"topic": "Обыкновенные дроби: понятие", "grade_min": 5, "grade_max": 6, "difficulty_min": 450, "difficulty_max": 550, "category": "Дроби"},
    {"topic": "Сравнение дробей", "grade_min": 5, "grade_max": 6, "difficulty_min": 475, "difficulty_max": 575, "category": "Дроби"},
    {"topic": "Сложение дробей с одинаковыми знаменателями", "grade_min": 5, "grade_max": 6, "difficulty_min": 500, "difficulty_max": 600, "category": "Дроби"},
    {"topic": "Вычитание дробей с одинаковыми знаменателями", "grade_min": 5, "grade_max": 6, "difficulty_min": 500, "difficulty_max": 600, "category": "Дроби"},
    {"topic": "Сложение дробей с разными знаменателями", "grade_min": 5, "grade_max": 6, "difficulty_min": 550, "difficulty_max": 650, "category": "Дроби"},
    {"topic": "Вычитание дробей с разными знаменателями", "grade_min": 5, "grade_max": 6, "difficulty_min": 550, "difficulty_max": 650, "category": "Дроби"},
    {"topic": "Умножение дробей", "grade_min": 5, "grade_max": 6, "difficulty_min": 525, "difficulty_max": 625, "category": "Дроби"},
    {"topic": "Деление дробей", "grade_min": 5, "grade_max": 6, "difficulty_min": 575, "difficulty_max": 675, "category": "Дроби"},
    {"topic": "Десятичные дроби: понятие", "grade_min": 5, "grade_max": 6, "difficulty_min": 450, "difficulty_max": 550, "category": "Дроби"},
    {"topic": "Сложение десятичных дробей", "grade_min": 5, "grade_max": 6, "difficulty_min": 475, "difficulty_max": 575, "category": "Дроби"},
    {"topic": "Вычитание десятичных дробей", "grade_min": 5, "grade_max": 6, "difficulty_min": 475, "difficulty_max": 575, "category": "Дроби"},
    {"topic": "Умножение десятичных дробей", "grade_min": 5, "grade_max": 6, "difficulty_min": 525, "difficulty_max": 625, "category": "Дроби"},
    {"topic": "Деление десятичных дробей", "grade_min": 5, "grade_max": 6, "difficulty_min": 575, "difficulty_max": 675, "category": "Дроби"},
    {"topic": "Проценты: понятие", "grade_min": 5, "grade_max": 6, "difficulty_min": 500, "difficulty_max": 600, "category": "Проценты"},
    {"topic": "Нахождение процента от числа", "grade_min": 5, "grade_max": 6, "difficulty_min": 525, "difficulty_max": 625, "category": "Проценты"},
    {"topic": "Нахождение числа по его проценту", "grade_min": 5, "grade_max": 7, "difficulty_min": 575, "difficulty_max": 675, "category": "Проценты"},
    {"topic": "Простые уравнения с одной переменной", "grade_min": 5, "grade_max": 6, "difficulty_min": 500, "difficulty_max": 600, "category": "Уравнения"},
    {"topic": "Уравнения с дробями", "grade_min": 5, "grade_max": 7, "difficulty_min": 600, "difficulty_max": 700, "category": "Уравнения"},
    {"topic": "Углы: виды углов", "grade_min": 5, "grade_max": 6, "difficulty_min": 450, "difficulty_max": 550, "category": "Геометрия"},
    {"topic": "Треугольник: виды треугольников", "grade_min": 5, "grade_max": 6, "difficulty_min": 475, "difficulty_max": 575, "category": "Геометрия"},
    {"topic": "Площадь треугольника", "grade_min": 5, "grade_max": 7, "difficulty_min": 550, "difficulty_max": 650, "category": "Геометрия"},
    {"topic": "Объем прямоугольного параллелепипеда", "grade_min": 5, "grade_max": 6, "difficulty_min": 525, "difficulty_max": 625, "category": "Геометрия"},
    {"topic": "Задачи на движение навстречу", "grade_min": 5, "grade_max": 7, "difficulty_min": 600, "difficulty_max": 700, "category": "Текстовые задачи"},
    {"topic": "Задачи на движение в одном направлении", "grade_min": 5, "grade_max": 7, "difficulty_min": 625, "difficulty_max": 725, "category": "Текстовые задачи"},
    
    # ==================== 6 КЛАСС (11-12 лет) ====================
    # Сложность: 500-900
    
    {"topic": "Делимость чисел", "grade_min": 6, "grade_max": 7, "difficulty_min": 500, "difficulty_max": 600, "category": "Арифметика"},
    {"topic": "НОД и НОК", "grade_min": 6, "grade_max": 7, "difficulty_min": 550, "difficulty_max": 650, "category": "Арифметика"},
    {"topic": "Простые и составные числа", "grade_min": 6, "grade_max": 7, "difficulty_min": 525, "difficulty_max": 625, "category": "Арифметика"},
    {"topic": "Отрицательные числа: понятие", "grade_min": 6, "grade_max": 7, "difficulty_min": 550, "difficulty_max": 650, "category": "Арифметика"},
    {"topic": "Сложение отрицательных чисел", "grade_min": 6, "grade_max": 7, "difficulty_min": 575, "difficulty_max": 675, "category": "Арифметика"},
    {"topic": "Вычитание отрицательных чисел", "grade_min": 6, "grade_max": 7, "difficulty_min": 600, "difficulty_max": 700, "category": "Арифметика"},
    {"topic": "Умножение отрицательных чисел", "grade_min": 6, "grade_max": 7, "difficulty_min": 625, "difficulty_max": 725, "category": "Арифметика"},
    {"topic": "Деление отрицательных чисел", "grade_min": 6, "grade_max": 7, "difficulty_min": 625, "difficulty_max": 725, "category": "Арифметика"},
    {"topic": "Координатная прямая", "grade_min": 6, "grade_max": 7, "difficulty_min": 550, "difficulty_max": 650, "category": "Координаты"},
    {"topic": "Координатная плоскость", "grade_min": 6, "grade_max": 7, "difficulty_min": 600, "difficulty_max": 700, "category": "Координаты"},
    {"topic": "Модуль числа", "grade_min": 6, "grade_max": 7, "difficulty_min": 575, "difficulty_max": 675, "category": "Арифметика"},
    {"topic": "Пропорции", "grade_min": 6, "grade_max": 7, "difficulty_min": 625, "difficulty_max": 725, "category": "Отношения"},
    {"topic": "Прямая и обратная пропорциональность", "grade_min": 6, "grade_max": 8, "difficulty_min": 675, "difficulty_max": 775, "category": "Отношения"},
    {"topic": "Масштаб", "grade_min": 6, "grade_max": 7, "difficulty_min": 600, "difficulty_max": 700, "category": "Отношения"},
    {"topic": "Длина окружности", "grade_min": 6, "grade_max": 7, "difficulty_min": 625, "difficulty_max": 725, "category": "Геометрия"},
    {"topic": "Площадь круга", "grade_min": 6, "grade_max": 7, "difficulty_min": 650, "difficulty_max": 750, "category": "Геометрия"},
    {"topic": "Задачи на проценты (сложные)", "grade_min": 6, "grade_max": 8, "difficulty_min": 700, "difficulty_max": 800, "category": "Текстовые задачи"},
    {"topic": "Задачи на смеси и сплавы", "grade_min": 6, "grade_max": 9, "difficulty_min": 750, "difficulty_max": 850, "category": "Текстовые задачи"},
    
    # ==================== 7 КЛАСС (12-13 лет) ====================
    # Сложность: 600-1100
    
    {"topic": "Алгебраические выражения", "grade_min": 7, "grade_max": 8, "difficulty_min": 600, "difficulty_max": 700, "category": "Алгебра"},
    {"topic": "Одночлены и многочлены", "grade_min": 7, "grade_max": 8, "difficulty_min": 650, "difficulty_max": 750, "category": "Алгебра"},
    {"topic": "Сложение и вычитание многочленов", "grade_min": 7, "grade_max": 8, "difficulty_min": 675, "difficulty_max": 775, "category": "Алгебра"},
    {"topic": "Умножение многочленов", "grade_min": 7, "grade_max": 8, "difficulty_min": 725, "difficulty_max": 825, "category": "Алгебра"},
    {"topic": "Формулы сокращенного умножения", "grade_min": 7, "grade_max": 8, "difficulty_min": 750, "difficulty_max": 850, "category": "Алгебра"},
    {"topic": "Разложение на множители", "grade_min": 7, "grade_max": 9, "difficulty_min": 775, "difficulty_max": 875, "category": "Алгебра"},
    {"topic": "Линейные уравнения", "grade_min": 7, "grade_max": 8, "difficulty_min": 650, "difficulty_max": 750, "category": "Уравнения"},
    {"topic": "Системы линейных уравнений", "grade_min": 7, "grade_max": 9, "difficulty_min": 800, "difficulty_max": 900, "category": "Уравнения"},
    {"topic": "Линейная функция", "grade_min": 7, "grade_max": 8, "difficulty_min": 700, "difficulty_max": 800, "category": "Функции"},
    {"topic": "График линейной функции", "grade_min": 7, "grade_max": 8, "difficulty_min": 725, "difficulty_max": 825, "category": "Функции"},
    {"topic": "Степень с натуральным показателем", "grade_min": 7, "grade_max": 8, "difficulty_min": 675, "difficulty_max": 775, "category": "Степени"},
    {"topic": "Свойства степеней", "grade_min": 7, "grade_max": 8, "difficulty_min": 725, "difficulty_max": 825, "category": "Степени"},
    {"topic": "Треугольники: признаки равенства", "grade_min": 7, "grade_max": 8, "difficulty_min": 700, "difficulty_max": 800, "category": "Геометрия"},
    {"topic": "Параллельные прямые", "grade_min": 7, "grade_max": 8, "difficulty_min": 675, "difficulty_max": 775, "category": "Геометрия"},
    {"topic": "Сумма углов треугольника", "grade_min": 7, "grade_max": 8, "difficulty_min": 700, "difficulty_max": 800, "category": "Геометрия"},
    {"topic": "Теорема Пифагора", "grade_min": 7, "grade_max": 9, "difficulty_min": 800, "difficulty_max": 900, "category": "Геометрия"},
    {"topic": "Статистика: среднее арифметическое", "grade_min": 7, "grade_max": 8, "difficulty_min": 650, "difficulty_max": 750, "category": "Статистика"},
    
    # ==================== 8 КЛАСС (13-14 лет) ====================
    # Сложность: 700-1300
    
    {"topic": "Рациональные дроби", "grade_min": 8, "grade_max": 9, "difficulty_min": 750, "difficulty_max": 850, "category": "Алгебра"},
    {"topic": "Сложение и вычитание рациональных дробей", "grade_min": 8, "grade_max": 9, "difficulty_min": 800, "difficulty_max": 900, "category": "Алгебра"},
    {"topic": "Умножение и деление рациональных дробей", "grade_min": 8, "grade_max": 9, "difficulty_min": 825, "difficulty_max": 925, "category": "Алгебра"},
    {"topic": "Квадратные корни", "grade_min": 8, "grade_max": 9, "difficulty_min": 775, "difficulty_max": 875, "category": "Корни"},
    {"topic": "Свойства квадратных корней", "grade_min": 8, "grade_max": 9, "difficulty_min": 825, "difficulty_max": 925, "category": "Корни"},
    {"topic": "Квадратные уравнения", "grade_min": 8, "grade_max": 9, "difficulty_min": 850, "difficulty_max": 950, "category": "Уравнения"},
    {"topic": "Теорема Виета", "grade_min": 8, "grade_max": 9, "difficulty_min": 875, "difficulty_max": 975, "category": "Уравнения"},
    {"topic": "Дробно-рациональные уравнения", "grade_min": 8, "grade_max": 10, "difficulty_min": 950, "difficulty_max": 1050, "category": "Уравнения"},
    {"topic": "Неравенства", "grade_min": 8, "grade_max": 9, "difficulty_min": 800, "difficulty_max": 900, "category": "Неравенства"},
    {"topic": "Системы неравенств", "grade_min": 8, "grade_max": 10, "difficulty_min": 900, "difficulty_max": 1000, "category": "Неравенства"},
    {"topic": "Степень с целым показателем", "grade_min": 8, "grade_max": 9, "difficulty_min": 775, "difficulty_max": 875, "category": "Степени"},
    {"topic": "Квадратичная функция", "grade_min": 8, "grade_max": 9, "difficulty_min": 850, "difficulty_max": 950, "category": "Функции"},
    {"topic": "Парабола", "grade_min": 8, "grade_max": 9, "difficulty_min": 875, "difficulty_max": 975, "category": "Функции"},
    {"topic": "Четырехугольники", "grade_min": 8, "grade_max": 9, "difficulty_min": 750, "difficulty_max": 850, "category": "Геометрия"},
    {"topic": "Площадь параллелограмма", "grade_min": 8, "grade_max": 9, "difficulty_min": 775, "difficulty_max": 875, "category": "Геометрия"},
    {"topic": "Площадь трапеции", "grade_min": 8, "grade_max": 9, "difficulty_min": 800, "difficulty_max": 900, "category": "Геометрия"},
    {"topic": "Подобные треугольники", "grade_min": 8, "grade_max": 9, "difficulty_min": 850, "difficulty_max": 950, "category": "Геометрия"},
    {"topic": "Окружность: вписанные углы", "grade_min": 8, "grade_max": 9, "difficulty_min": 825, "difficulty_max": 925, "category": "Геометрия"},
    
    # ==================== 9 КЛАСС (14-15 лет) ====================
    # Сложность: 800-1500
    
    {"topic": "Квадратичные неравенства", "grade_min": 9, "grade_max": 10, "difficulty_min": 950, "difficulty_max": 1050, "category": "Неравенства"},
    {"topic": "Метод интервалов", "grade_min": 9, "grade_max": 11, "difficulty_min": 1000, "difficulty_max": 1100, "category": "Неравенства"},
    {"topic": "Уравнения высших степеней", "grade_min": 9, "grade_max": 11, "difficulty_min": 1050, "difficulty_max": 1150, "category": "Уравнения"},
    {"topic": "Иррациональные уравнения", "grade_min": 9, "grade_max": 11, "difficulty_min": 1100, "difficulty_max": 1200, "category": "Уравнения"},
    {"topic": "Системы уравнений второй степени", "grade_min": 9, "grade_max": 10, "difficulty_min": 1050, "difficulty_max": 1150, "category": "Уравнения"},
    {"topic": "Арифметическая прогрессия", "grade_min": 9, "grade_max": 10, "difficulty_min": 900, "difficulty_max": 1000, "category": "Последовательности"},
    {"topic": "Геометрическая прогрессия", "grade_min": 9, "grade_max": 10, "difficulty_min": 950, "difficulty_max": 1050, "category": "Последовательности"},
    {"topic": "Степенная функция", "grade_min": 9, "grade_max": 10, "difficulty_min": 900, "difficulty_max": 1000, "category": "Функции"},
    {"topic": "Корень n-ой степени", "grade_min": 9, "grade_max": 11, "difficulty_min": 950, "difficulty_max": 1050, "category": "Корни"},
    {"topic": "Векторы на плоскости", "grade_min": 9, "grade_max": 10, "difficulty_min": 875, "difficulty_max": 975, "category": "Геометрия"},
    {"topic": "Скалярное произведение векторов", "grade_min": 9, "grade_max": 11, "difficulty_min": 950, "difficulty_max": 1050, "category": "Геометрия"},
    {"topic": "Правильные многоугольники", "grade_min": 9, "grade_max": 10, "difficulty_min": 875, "difficulty_max": 975, "category": "Геометрия"},
    {"topic": "Длина окружности и площадь круга (углубленно)", "grade_min": 9, "grade_max": 10, "difficulty_min": 900, "difficulty_max": 1000, "category": "Геометрия"},
    {"topic": "Элементы комбинаторики", "grade_min": 9, "grade_max": 11, "difficulty_min": 1000, "difficulty_max": 1100, "category": "Комбинаторика"},
    {"topic": "Теория вероятностей: основы", "grade_min": 9, "grade_max": 11, "difficulty_min": 950, "difficulty_max": 1050, "category": "Вероятность"},
    
    # ==================== 10 КЛАСС (15-16 лет) ====================
    # Сложность: 900-1800
    
    {"topic": "Тригонометрические функции", "grade_min": 10, "grade_max": 11, "difficulty_min": 1000, "difficulty_max": 1200, "category": "Тригонометрия"},
    {"topic": "Тригонометрические уравнения", "grade_min": 10, "grade_max": 11, "difficulty_min": 1100, "difficulty_max": 1300, "category": "Тригонометрия"},
    {"topic": "Обратные тригонометрические функции", "grade_min": 10, "grade_max": 11, "difficulty_min": 1150, "difficulty_max": 1350, "category": "Тригонометрия"},
    {"topic": "Преобразование тригонометрических выражений", "grade_min": 10, "grade_max": 11, "difficulty_min": 1200, "difficulty_max": 1400, "category": "Тригонометрия"},
    {"topic": "Показательная функция", "grade_min": 10, "grade_max": 11, "difficulty_min": 1050, "difficulty_max": 1250, "category": "Функции"},
    {"topic": "Показательные уравнения", "grade_min": 10, "grade_max": 11, "difficulty_min": 1150, "difficulty_max": 1350, "category": "Уравнения"},
    {"topic": "Показательные неравенства", "grade_min": 10, "grade_max": 11, "difficulty_min": 1200, "difficulty_max": 1400, "category": "Неравенства"},
    {"topic": "Логарифмическая функция", "grade_min": 10, "grade_max": 11, "difficulty_min": 1100, "difficulty_max": 1300, "category": "Функции"},
    {"topic": "Логарифмические уравнения", "grade_min": 10, "grade_max": 11, "difficulty_min": 1200, "difficulty_max": 1400, "category": "Уравнения"},
    {"topic": "Логарифмические неравенства", "grade_min": 10, "grade_max": 11, "difficulty_min": 1250, "difficulty_max": 1450, "category": "Неравенства"},
    {"topic": "Производная функции", "grade_min": 10, "grade_max": 11, "difficulty_min": 1150, "difficulty_max": 1350, "category": "Производная"},
    {"topic": "Правила дифференцирования", "grade_min": 10, "grade_max": 11, "difficulty_min": 1200, "difficulty_max": 1400, "category": "Производная"},
    {"topic": "Применение производной", "grade_min": 10, "grade_max": 11, "difficulty_min": 1250, "difficulty_max": 1450, "category": "Производная"},
    {"topic": "Исследование функций", "grade_min": 10, "grade_max": 11, "difficulty_min": 1300, "difficulty_max": 1500, "category": "Функции"},
    {"topic": "Параллелепипед и призма", "grade_min": 10, "grade_max": 11, "difficulty_min": 1000, "difficulty_max": 1200, "category": "Стереометрия"},
    {"topic": "Пирамида", "grade_min": 10, "grade_max": 11, "difficulty_min": 1050, "difficulty_max": 1250, "category": "Стереометрия"},
    {"topic": "Цилиндр", "grade_min": 10, "grade_max": 11, "difficulty_min": 1100, "difficulty_max": 1300, "category": "Стереометрия"},
    {"topic": "Конус", "grade_min": 10, "grade_max": 11, "difficulty_min": 1150, "difficulty_max": 1350, "category": "Стереометрия"},
    {"topic": "Сфера и шар", "grade_min": 10, "grade_max": 11, "difficulty_min": 1200, "difficulty_max": 1400, "category": "Стереометрия"},
    
    # ==================== 11 КЛАСС (16-17 лет) ====================
    # Сложность: 1000-2000
    
    {"topic": "Первообразная и интеграл", "grade_min": 11, "grade_max": 11, "difficulty_min": 1300, "difficulty_max": 1500, "category": "Интегралы"},
    {"topic": "Определенный интеграл", "grade_min": 11, "grade_max": 11, "difficulty_min": 1350, "difficulty_max": 1550, "category": "Интегралы"},
    {"topic": "Площадь криволинейной трапеции", "grade_min": 11, "grade_max": 11, "difficulty_min": 1400, "difficulty_max": 1600, "category": "Интегралы"},
    {"topic": "Комбинаторика: перестановки", "grade_min": 11, "grade_max": 11, "difficulty_min": 1200, "difficulty_max": 1400, "category": "Комбинаторика"},
    {"topic": "Комбинаторика: размещения", "grade_min": 11, "grade_max": 11, "difficulty_min": 1250, "difficulty_max": 1450, "category": "Комбинаторика"},
    {"topic": "Комбинаторика: сочетания", "grade_min": 11, "grade_max": 11, "difficulty_min": 1300, "difficulty_max": 1500, "category": "Комбинаторика"},
    {"topic": "Бином Ньютона", "grade_min": 11, "grade_max": 11, "difficulty_min": 1350, "difficulty_max": 1550, "category": "Комбинаторика"},
    {"topic": "Вероятность события", "grade_min": 11, "grade_max": 11, "difficulty_min": 1200, "difficulty_max": 1400, "category": "Вероятность"},
    {"topic": "Условная вероятность", "grade_min": 11, "grade_max": 11, "difficulty_min": 1300, "difficulty_max": 1500, "category": "Вероятность"},
    {"topic": "Математическое ожидание", "grade_min": 11, "grade_max": 11, "difficulty_min": 1350, "difficulty_max": 1550, "category": "Вероятность"},
    {"topic": "Дисперсия", "grade_min": 11, "grade_max": 11, "difficulty_min": 1400, "difficulty_max": 1600, "category": "Вероятность"},
    {"topic": "Объемы многогранников", "grade_min": 11, "grade_max": 11, "difficulty_min": 1250, "difficulty_max": 1450, "category": "Стереометрия"},
    {"topic": "Объемы тел вращения", "grade_min": 11, "grade_max": 11, "difficulty_min": 1300, "difficulty_max": 1500, "category": "Стереометрия"},
    {"topic": "Векторы в пространстве", "grade_min": 11, "grade_max": 11, "difficulty_min": 1200, "difficulty_max": 1400, "category": "Стереометрия"},
    {"topic": "Метод координат в пространстве", "grade_min": 11, "grade_max": 11, "difficulty_min": 1300, "difficulty_max": 1500, "category": "Стереометрия"},
    
    # ==================== ОЛИМПИАДНАЯ МАТЕМАТИКА ====================
    # Сложность: 1500-2500
    
    {"topic": "Диофантовы уравнения", "grade_min": 9, "grade_max": 11, "difficulty_min": 1500, "difficulty_max": 1800, "category": "Олимпиадная"},
    {"topic": "Теория чисел: делимость", "grade_min": 8, "grade_max": 11, "difficulty_min": 1400, "difficulty_max": 1700, "category": "Олимпиадная"},
    {"topic": "Принцип Дирихле", "grade_min": 7, "grade_max": 11, "difficulty_min": 1600, "difficulty_max": 1900, "category": "Олимпиадная"},
    {"topic": "Инвариант", "grade_min": 8, "grade_max": 11, "difficulty_min": 1700, "difficulty_max": 2000, "category": "Олимпиадная"},
    {"topic": "Раскраски", "grade_min": 7, "grade_max": 11, "difficulty_min": 1500, "difficulty_max": 1800, "category": "Олимпиадная"},
    {"topic": "Графы", "grade_min": 8, "grade_max": 11, "difficulty_min": 1600, "difficulty_max": 1900, "category": "Олимпиадная"},
    {"topic": "Игры и стратегии", "grade_min": 7, "grade_max": 11, "difficulty_min": 1700, "difficulty_max": 2000, "category": "Олимпиадная"},
    {"topic": "Геометрические неравенства", "grade_min": 9, "grade_max": 11, "difficulty_min": 1800, "difficulty_max": 2100, "category": "Олимпиадная"},
    {"topic": "Функциональные уравнения", "grade_min": 10, "grade_max": 11, "difficulty_min": 1900, "difficulty_max": 2200, "category": "Олимпиадная"},
    {"topic": "Неравенство Коши", "grade_min": 9, "grade_max": 11, "difficulty_min": 1700, "difficulty_max": 2000, "category": "Олимпиадная"},
    {"topic": "Метод математической индукции", "grade_min": 9, "grade_max": 11, "difficulty_min": 1600, "difficulty_max": 1900, "category": "Олимпиадная"},
    
    # ==================== ПРОФЕССИОНАЛЬНЫЙ УРОВЕНЬ ====================
    # Сложность: 2000-3000
    
    {"topic": "Теория групп: основы", "grade_min": 11, "grade_max": 12, "difficulty_min": 2000, "difficulty_max": 2300, "category": "Высшая математика"},
    {"topic": "Теория колец", "grade_min": 11, "grade_max": 12, "difficulty_min": 2100, "difficulty_max": 2400, "category": "Высшая математика"},
    {"topic": "Линейная алгебра: матрицы", "grade_min": 11, "grade_max": 12, "difficulty_min": 1800, "difficulty_max": 2100, "category": "Высшая математика"},
    {"topic": "Определители", "grade_min": 11, "grade_max": 12, "difficulty_min": 1900, "difficulty_max": 2200, "category": "Высшая математика"},
    {"topic": "Системы линейных уравнений (метод Гаусса)", "grade_min": 11, "grade_max": 12, "difficulty_min": 1850, "difficulty_max": 2150, "category": "Высшая математика"},
    {"topic": "Векторные пространства", "grade_min": 11, "grade_max": 12, "difficulty_min": 2000, "difficulty_max": 2300, "category": "Высшая математика"},
    {"topic": "Линейные операторы", "grade_min": 11, "grade_max": 12, "difficulty_min": 2100, "difficulty_max": 2400, "category": "Высшая математика"},
    {"topic": "Собственные значения и векторы", "grade_min": 11, "grade_max": 12, "difficulty_min": 2150, "difficulty_max": 2450, "category": "Высшая математика"},
    {"topic": "Пределы последовательностей", "grade_min": 11, "grade_max": 12, "difficulty_min": 1900, "difficulty_max": 2200, "category": "Математический анализ"},
    {"topic": "Пределы функций", "grade_min": 11, "grade_max": 12, "difficulty_min": 1950, "difficulty_max": 2250, "category": "Математический анализ"},
    {"topic": "Непрерывность функций", "grade_min": 11, "grade_max": 12, "difficulty_min": 2000, "difficulty_max": 2300, "category": "Математический анализ"},
    {"topic": "Дифференциальное исчисление", "grade_min": 11, "grade_max": 12, "difficulty_min": 2050, "difficulty_max": 2350, "category": "Математический анализ"},
    {"topic": "Интегральное исчисление", "grade_min": 11, "grade_max": 12, "difficulty_min": 2100, "difficulty_max": 2400, "category": "Математический анализ"},
    {"topic": "Ряды", "grade_min": 11, "grade_max": 12, "difficulty_min": 2150, "difficulty_max": 2450, "category": "Математический анализ"},
    {"topic": "Дифференциальные уравнения первого порядка", "grade_min": 11, "grade_max": 12, "difficulty_min": 2200, "difficulty_max": 2500, "category": "Дифференциальные уравнения"},
    {"topic": "Дифференциальные уравнения второго порядка", "grade_min": 11, "grade_max": 12, "difficulty_min": 2300, "difficulty_max": 2600, "category": "Дифференциальные уравнения"},
    {"topic": "Комплексные числа", "grade_min": 11, "grade_max": 12, "difficulty_min": 1900, "difficulty_max": 2200, "category": "Комплексный анализ"},
    {"topic": "Функции комплексной переменной", "grade_min": 11, "grade_max": 12, "difficulty_min": 2100, "difficulty_max": 2400, "category": "Комплексный анализ"},
    {"topic": "Аналитическая геометрия", "grade_min": 11, "grade_max": 12, "difficulty_min": 1950, "difficulty_max": 2250, "category": "Геометрия"},
    {"topic": "Кривые второго порядка", "grade_min": 11, "grade_max": 12, "difficulty_min": 2050, "difficulty_max": 2350, "category": "Геометрия"},
]

# Генерация дополнительных тем программно для достижения 1000+
def _generate_additional_topics():
    """Генерирует дополнительные темы для расширения базы"""
    additional = []
    
    # Дополнительные темы для каждого класса с вариациями
    
    # 1-2 класс - вариации базовых операций
    for i in range(1, 11):
        additional.append({"topic": f"Сложение чисел до {i*10}", "grade_min": 1, "grade_max": 2, "difficulty_min": i*10, "difficulty_max": i*10+50, "category": "Арифметика"})
        additional.append({"topic": f"Вычитание чисел до {i*10}", "grade_min": 1, "grade_max": 2, "difficulty_min": i*10, "difficulty_max": i*10+50, "category": "Арифметика"})
    
    # 3-4 класс - таблица умножения и деления
    for i in range(2, 13):
        additional.append({"topic": f"Умножение на {i} (расширенное)", "grade_min": 3, "grade_max": 4, "difficulty_min": 200+i*10, "difficulty_max": 300+i*10, "category": "Арифметика"})
        additional.append({"topic": f"Деление на {i} (расширенное)", "grade_min": 3, "grade_max": 4, "difficulty_min": 225+i*10, "difficulty_max": 325+i*10, "category": "Арифметика"})
    
    # 5-6 класс - дроби с разными знаменателями
    denominators = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30, 50, 100]
    for d in denominators:
        additional.append({"topic": f"Дроби со знаменателем {d}", "grade_min": 5, "grade_max": 6, "difficulty_min": 450+d, "difficulty_max": 550+d, "category": "Дроби"})
    
    # 5-7 класс - проценты (разные типы задач)
    percent_types = [
        "Нахождение процента от числа (простые)",
        "Нахождение процента от числа (сложные)",
        "Нахождение числа по проценту (простые)",
        "Нахождение числа по проценту (сложные)",
        "Процентное соотношение",
        "Увеличение на процент",
        "Уменьшение на процент",
        "Последовательное изменение на проценты",
        "Сложные проценты",
        "Задачи на скидки",
        "Задачи на наценку",
        "Задачи на распродажи"
    ]
    for idx, ptype in enumerate(percent_types):
        additional.append({"topic": ptype, "grade_min": 5, "grade_max": 7, "difficulty_min": 500+idx*25, "difficulty_max": 650+idx*25, "category": "Проценты"})
    
    # 6-9 класс - текстовые задачи на движение (вариации)
    movement_types = [
        "Задачи на движение по прямой",
        "Задачи на движение по окружности",
        "Задачи на движение по реке",
        "Задачи на движение с остановками",
        "Задачи на среднюю скорость",
        "Задачи на обгон",
        "Задачи на встречное движение (сложные)",
        "Задачи на движение в противоположных направлениях",
        "Задачи на движение с изменением скорости",
        "Задачи на движение нескольких объектов"
    ]
    for idx, mtype in enumerate(movement_types):
        additional.append({"topic": mtype, "grade_min": 6, "grade_max": 9, "difficulty_min": 600+idx*30, "difficulty_max": 750+idx*30, "category": "Текстовые задачи"})
    
    # 7-9 класс - уравнения (разные типы)
    equation_types = [
        "Линейные уравнения с одной переменной (сложные)",
        "Линейные уравнения с дробями",
        "Линейные уравнения с модулем",
        "Квадратные уравнения (полные)",
        "Квадратные уравнения (неполные)",
        "Квадратные уравнения с параметром",
        "Биквадратные уравнения",
        "Уравнения, приводимые к квадратным",
        "Дробно-рациональные уравнения (простые)",
        "Дробно-рациональные уравнения (сложные)",
        "Иррациональные уравнения (простые)",
        "Иррациональные уравнения (с двумя корнями)",
        "Иррациональные уравнения (сложные)",
        "Системы линейных уравнений (2 уравнения)",
        "Системы линейных уравнений (3 уравнения)",
        "Системы нелинейных уравнений"
    ]
    for idx, etype in enumerate(equation_types):
        additional.append({"topic": etype, "grade_min": 7, "grade_max": 10, "difficulty_min": 700+idx*40, "difficulty_max": 900+idx*40, "category": "Уравнения"})
    
    # 8-10 класс - неравенства
    inequality_types = [
        "Линейные неравенства",
        "Квадратные неравенства (простые)",
        "Квадратные неравенства (сложные)",
        "Рациональные неравенства",
        "Иррациональные неравенства",
        "Показательные неравенства (простые)",
        "Показательные неравенства (сложные)",
        "Логарифмические неравенства (простые)",
        "Логарифмические неравенства (сложные)",
        "Системы неравенств (2 неравенства)",
        "Системы неравенств (3+ неравенства)",
        "Неравенства с модулем",
        "Неравенства с параметром"
    ]
    for idx, itype in enumerate(inequality_types):
        additional.append({"topic": itype, "grade_min": 8, "grade_max": 11, "difficulty_min": 800+idx*50, "difficulty_max": 1000+idx*50, "category": "Неравенства"})
    
    # 7-11 класс - геометрия планиметрия
    geometry_plane = [
        "Треугольники: медианы",
        "Треугольники: биссектрисы",
        "Треугольники: высоты",
        "Треугольники: средние линии",
        "Прямоугольные треугольники",
        "Равнобедренные треугольники",
        "Равносторонние треугольники",
        "Подобие треугольников",
        "Четырехугольники: параллелограмм",
        "Четырехугольники: ромб",
        "Четырехугольники: трапеция",
        "Четырехугольники: прямоугольник",
        "Четырехугольники: квадрат",
        "Вписанные и описанные окружности",
        "Касательные к окружности",
        "Хорды окружности",
        "Секущие окружности",
        "Центральные углы",
        "Вписанные углы (расширенное)",
        "Площади многоугольников"
    ]
    for idx, gtype in enumerate(geometry_plane):
        additional.append({"topic": gtype, "grade_min": 7, "grade_max": 9, "difficulty_min": 700+idx*30, "difficulty_max": 900+idx*30, "category": "Геометрия"})
    
    # 10-11 класс - стереометрия
    geometry_space = [
        "Призма: правильная",
        "Призма: наклонная",
        "Пирамида: правильная",
        "Пирамида: усеченная",
        "Тетраэдр",
        "Октаэдр",
        "Куб (расширенное)",
        "Параллелепипед (расширенное)",
        "Цилиндр: площадь поверхности",
        "Цилиндр: объем",
        "Конус: площадь поверхности",
        "Конус: объем",
        "Усеченный конус",
        "Сфера: площадь",
        "Шар: объем",
        "Комбинации тел",
        "Сечения многогранников",
        "Расстояния в пространстве",
        "Углы в пространстве"
    ]
    for idx, stype in enumerate(geometry_space):
        additional.append({"topic": stype, "grade_min": 10, "grade_max": 11, "difficulty_min": 1100+idx*40, "difficulty_max": 1400+idx*40, "category": "Стереометрия"})
    
    # 10-11 класс - тригонометрия
    trig_types = [
        "Синус угла",
        "Косинус угла",
        "Тангенс угла",
        "Котангенс угла",
        "Тригонометрические тождества (основные)",
        "Тригонометрические тождества (сложные)",
        "Формулы приведения",
        "Формулы двойного угла",
        "Формулы половинного угла",
        "Формулы суммы и разности",
        "Формулы произведения",
        "Простейшие тригонометрические уравнения",
        "Тригонометрические уравнения (однородные)",
        "Тригонометрические уравнения (с заменой)",
        "Тригонометрические уравнения (сложные)",
        "Обратные тригонометрические функции (arcsin)",
        "Обратные тригонометрические функции (arccos)",
        "Обратные тригонометрические функции (arctg)",
        "Обратные тригонометрические функции (arcctg)"
    ]
    for idx, ttype in enumerate(trig_types):
        additional.append({"topic": ttype, "grade_min": 10, "grade_max": 11, "difficulty_min": 1000+idx*50, "difficulty_max": 1300+idx*50, "category": "Тригонометрия"})
    
    # 10-11 класс - показательные и логарифмы
    exp_log_types = [
        "Свойства степеней (расширенное)",
        "Показательная функция: график",
        "Показательная функция: свойства",
        "Показательные уравнения (базовые)",
        "Показательные уравнения (с заменой)",
        "Показательные уравнения (системы)",
        "Логарифм: определение",
        "Свойства логарифмов",
        "Логарифмическая функция: график",
        "Логарифмическая функция: свойства",
        "Логарифмические уравнения (базовые)",
        "Логарифмические уравнения (с заменой)",
        "Логарифмические уравнения (системы)",
        "Смешанные показательно-логарифмические уравнения"
    ]
    for idx, eltype in enumerate(exp_log_types):
        additional.append({"topic": eltype, "grade_min": 10, "grade_max": 11, "difficulty_min": 1100+idx*60, "difficulty_max": 1400+idx*60, "category": "Функции"})
    
    # 10-11 класс - производная и интеграл
    calculus_types = [
        "Производная: определение",
        "Производная константы",
        "Производная степенной функции",
        "Производная показательной функции",
        "Производная логарифмической функции",
        "Производная тригонометрических функций",
        "Производная сложной функции",
        "Производная произведения",
        "Производная частного",
        "Геометрический смысл производной",
        "Физический смысл производной",
        "Уравнение касательной",
        "Возрастание и убывание функции",
        "Экстремумы функции",
        "Наибольшее и наименьшее значение",
        "Выпуклость функции",
        "Точки перегиба",
        "Асимптоты",
        "Первообразная: определение",
        "Первообразная степенной функции",
        "Первообразная показательной функции",
        "Первообразная тригонометрических функций",
        "Неопределенный интеграл",
        "Определенный интеграл: вычисление",
        "Определенный интеграл: свойства",
        "Площадь фигуры через интеграл",
        "Объем тела вращения"
    ]
    for idx, ctype in enumerate(calculus_types):
        additional.append({"topic": ctype, "grade_min": 10, "grade_max": 11, "difficulty_min": 1200+idx*40, "difficulty_max": 1500+idx*40, "category": "Производная" if idx < 18 else "Интегралы"})
    
    # 9-11 класс - комбинаторика и вероятность
    prob_comb_types = [
        "Правило суммы",
        "Правило произведения",
        "Перестановки без повторений",
        "Перестановки с повторениями",
        "Размещения без повторений",
        "Размещения с повторениями",
        "Сочетания без повторений",
        "Сочетания с повторениями",
        "Треугольник Паскаля",
        "Классическое определение вероятности",
        "Геометрическая вероятность",
        "Теоремы сложения вероятностей",
        "Теоремы умножения вероятностей",
        "Независимые события",
        "Зависимые события",
        "Формула полной вероятности",
        "Формула Байеса",
        "Схема Бернулли",
        "Случайные величины",
        "Закон распределения"
    ]
    for idx, pctype in enumerate(prob_comb_types):
        additional.append({"topic": pctype, "grade_min": 9, "grade_max": 11, "difficulty_min": 1000+idx*50, "difficulty_max": 1300+idx*50, "category": "Комбинаторика" if idx < 9 else "Вероятность"})
    
    # Олимпиадные темы (расширенные)
    olympiad_types = [
        "Делимость: признаки делимости",
        "Делимость: НОД и НОК (олимпиадные)",
        "Простые числа: решето Эратосфена",
        "Простые числа: распределение",
        "Сравнения по модулю",
        "Малая теорема Ферма",
        "Теорема Эйлера",
        "Китайская теорема об остатках",
        "Уравнения в целых числах (линейные)",
        "Уравнения в целых числах (квадратные)",
        "Принцип крайнего",
        "Принцип узких мест",
        "Метод раскрасок (шахматная)",
        "Метод раскрасок (произвольная)",
        "Графы: основные понятия",
        "Графы: эйлеровы пути",
        "Графы: гамильтоновы циклы",
        "Графы: деревья",
        "Комбинаторная геометрия",
        "Неравенство треугольника (олимпиадное)",
        "Неравенство о средних",
        "Неравенство Коши-Буняковского",
        "Неравенство Чебышева",
        "Выпуклые многоугольники",
        "Площади и объемы (олимпиадные)",
        "Геометрические места точек",
        "Гомотетия",
        "Инверсия",
        "Проективная геометрия",
        "Аффинные преобразования"
    ]
    for idx, otype in enumerate(olympiad_types):
        additional.append({"topic": otype, "grade_min": 8, "grade_max": 11, "difficulty_min": 1500+idx*30, "difficulty_max": 2000+idx*30, "category": "Олимпиадная"})
    
    # Дополнительные вариации для всех уровней
    # Еще больше задач для начальной школы (1-4 класс)
    for i in range(1, 21):
        additional.append({"topic": f"Задачи на сложение (уровень {i})", "grade_min": 1, "grade_max": 3, "difficulty_min": 50+i*10, "difficulty_max": 150+i*10, "category": "Текстовые задачи"})
        additional.append({"topic": f"Задачи на вычитание (уровень {i})", "grade_min": 1, "grade_max": 3, "difficulty_min": 50+i*10, "difficulty_max": 150+i*10, "category": "Текстовые задачи"})
    
    # Задачи на умножение и деление (3-5 класс)
    for i in range(1, 21):
        additional.append({"topic": f"Задачи на умножение (уровень {i})", "grade_min": 3, "grade_max": 5, "difficulty_min": 200+i*15, "difficulty_max": 350+i*15, "category": "Текстовые задачи"})
        additional.append({"topic": f"Задачи на деление (уровень {i})", "grade_min": 3, "grade_max": 5, "difficulty_min": 225+i*15, "difficulty_max": 375+i*15, "category": "Текстовые задачи"})
    
    # Задачи с дробями (5-7 класс)
    for i in range(1, 21):
        additional.append({"topic": f"Задачи с обыкновенными дробями (уровень {i})", "grade_min": 5, "grade_max": 7, "difficulty_min": 450+i*20, "difficulty_max": 650+i*20, "category": "Текстовые задачи"})
        additional.append({"topic": f"Задачи с десятичными дробями (уровень {i})", "grade_min": 5, "grade_max": 7, "difficulty_min": 475+i*20, "difficulty_max": 675+i*20, "category": "Текстовые задачи"})
    
    # Задачи на проценты (вариации по сложности)
    for i in range(1, 16):
        additional.append({"topic": f"Задачи на проценты (сложность {i})", "grade_min": 5, "grade_max": 8, "difficulty_min": 500+i*30, "difficulty_max": 700+i*30, "category": "Текстовые задачи"})
    
    # Задачи на пропорции
    for i in range(1, 11):
        additional.append({"topic": f"Задачи на пропорции (уровень {i})", "grade_min": 6, "grade_max": 8, "difficulty_min": 600+i*25, "difficulty_max": 750+i*25, "category": "Текстовые задачи"})
    
    # Задачи на работу
    for i in range(1, 11):
        additional.append({"topic": f"Задачи на совместную работу (уровень {i})", "grade_min": 6, "grade_max": 9, "difficulty_min": 650+i*30, "difficulty_max": 850+i*30, "category": "Текстовые задачи"})
    
    # Задачи на смеси и сплавы (вариации)
    for i in range(1, 11):
        additional.append({"topic": f"Задачи на смеси (уровень {i})", "grade_min": 7, "grade_max": 10, "difficulty_min": 750+i*40, "difficulty_max": 950+i*40, "category": "Текстовые задачи"})
        additional.append({"topic": f"Задачи на сплавы (уровень {i})", "grade_min": 7, "grade_max": 10, "difficulty_min": 775+i*40, "difficulty_max": 975+i*40, "category": "Текстовые задачи"})
    
    # Геометрические задачи (планиметрия - вариации)
    for i in range(1, 16):
        additional.append({"topic": f"Задачи на треугольники (сложность {i})", "grade_min": 7, "grade_max": 9, "difficulty_min": 700+i*35, "difficulty_max": 900+i*35, "category": "Геометрия"})
        additional.append({"topic": f"Задачи на четырехугольники (сложность {i})", "grade_min": 7, "grade_max": 9, "difficulty_min": 725+i*35, "difficulty_max": 925+i*35, "category": "Геометрия"})
        additional.append({"topic": f"Задачи на окружности (сложность {i})", "grade_min": 7, "grade_max": 9, "difficulty_min": 750+i*35, "difficulty_max": 950+i*35, "category": "Геометрия"})
    
    # Стереометрические задачи (вариации)
    for i in range(1, 16):
        additional.append({"topic": f"Задачи на многогранники (сложность {i})", "grade_min": 10, "grade_max": 11, "difficulty_min": 1100+i*45, "difficulty_max": 1400+i*45, "category": "Стереометрия"})
        additional.append({"topic": f"Задачи на тела вращения (сложность {i})", "grade_min": 10, "grade_max": 11, "difficulty_min": 1150+i*45, "difficulty_max": 1450+i*45, "category": "Стереометрия"})
    
    # Алгебраические выражения (вариации)
    for i in range(1, 16):
        additional.append({"topic": f"Упрощение выражений (сложность {i})", "grade_min": 7, "grade_max": 9, "difficulty_min": 650+i*30, "difficulty_max": 850+i*30, "category": "Алгебра"})
        additional.append({"topic": f"Разложение на множители (сложность {i})", "grade_min": 7, "grade_max": 9, "difficulty_min": 700+i*35, "difficulty_max": 900+i*35, "category": "Алгебра"})
    
    # Функции (вариации)
    for i in range(1, 11):
        additional.append({"topic": f"Построение графиков функций (уровень {i})", "grade_min": 7, "grade_max": 10, "difficulty_min": 700+i*40, "difficulty_max": 950+i*40, "category": "Функции"})
        additional.append({"topic": f"Преобразование графиков (уровень {i})", "grade_min": 8, "grade_max": 10, "difficulty_min": 800+i*45, "difficulty_max": 1050+i*45, "category": "Функции"})
    
    # Дополнительные темы для достижения 1000+
    # Уравнения (расширенные вариации)
    for i in range(1, 21):
        additional.append({"topic": f"Линейные уравнения (вариация {i})", "grade_min": 7, "grade_max": 8, "difficulty_min": 650+i*20, "difficulty_max": 800+i*20, "category": "Уравнения"})
    
    for i in range(1, 16):
        additional.append({"topic": f"Квадратные уравнения (вариация {i})", "grade_min": 8, "grade_max": 9, "difficulty_min": 850+i*30, "difficulty_max": 1050+i*30, "category": "Уравнения"})
    
    # Неравенства (расширенные)
    for i in range(1, 16):
        additional.append({"topic": f"Решение неравенств (сложность {i})", "grade_min": 8, "grade_max": 10, "difficulty_min": 800+i*35, "difficulty_max": 1000+i*35, "category": "Неравенства"})
    
    # Тригонометрия (расширенные вариации)
    for i in range(1, 16):
        additional.append({"topic": f"Тригонометрические уравнения (вариация {i})", "grade_min": 10, "grade_max": 11, "difficulty_min": 1100+i*40, "difficulty_max": 1350+i*40, "category": "Тригонометрия"})
    
    # Производная (практические задачи)
    for i in range(1, 16):
        additional.append({"topic": f"Применение производной (задача {i})", "grade_min": 10, "grade_max": 11, "difficulty_min": 1200+i*35, "difficulty_max": 1450+i*35, "category": "Производная"})
    
    # Интегралы (вариации)
    for i in range(1, 16):
        additional.append({"topic": f"Вычисление интегралов (сложность {i})", "grade_min": 11, "grade_max": 11, "difficulty_min": 1300+i*40, "difficulty_max": 1550+i*40, "category": "Интегралы"})
    
    # Комбинаторика и вероятность (расширенные)
    for i in range(1, 11):
        additional.append({"topic": f"Комбинаторные задачи (уровень {i})", "grade_min": 9, "grade_max": 11, "difficulty_min": 1000+i*45, "difficulty_max": 1250+i*45, "category": "Комбинаторика"})
        additional.append({"topic": f"Задачи на вероятность (уровень {i})", "grade_min": 9, "grade_max": 11, "difficulty_min": 1050+i*45, "difficulty_max": 1300+i*45, "category": "Вероятность"})
    
    # Финальные темы для превышения 1000
    # Логарифмы и показательные (вариации)
    for i in range(1, 11):
        additional.append({"topic": f"Показательные уравнения (вариация {i})", "grade_min": 10, "grade_max": 11, "difficulty_min": 1150+i*40, "difficulty_max": 1400+i*40, "category": "Уравнения"})
        additional.append({"topic": f"Логарифмические уравнения (вариация {i})", "grade_min": 10, "grade_max": 11, "difficulty_min": 1200+i*40, "difficulty_max": 1450+i*40, "category": "Уравнения"})
    
    # Системы уравнений (вариации)
    for i in range(1, 11):
        additional.append({"topic": f"Системы уравнений (сложность {i})", "grade_min": 7, "grade_max": 10, "difficulty_min": 800+i*35, "difficulty_max": 1050+i*35, "category": "Уравнения"})
    
    # Задачи на прогрессии
    for i in range(1, 11):
        additional.append({"topic": f"Арифметическая прогрессия (задача {i})", "grade_min": 9, "grade_max": 10, "difficulty_min": 900+i*30, "difficulty_max": 1100+i*30, "category": "Последовательности"})
        additional.append({"topic": f"Геометрическая прогрессия (задача {i})", "grade_min": 9, "grade_max": 10, "difficulty_min": 950+i*30, "difficulty_max": 1150+i*30, "category": "Последовательности"})
    
    # Высшая математика (расширенная)
    advanced_types = [
        "Множества и операции над ними",
        "Отображения и функции",
        "Бинарные отношения",
        "Отношения эквивалентности",
        "Отношения порядка",
        "Мощность множества",
        "Счетные множества",
        "Континуум",
        "Аксиома выбора",
        "Алгебраические структуры",
        "Группы: подгруппы",
        "Группы: гомоморфизмы",
        "Группы: изоморфизмы",
        "Кольца: идеалы",
        "Поля",
        "Многочлены над полем",
        "Разложение многочленов",
        "Корни многочленов",
        "Матрицы: операции",
        "Матрицы: обратная матрица",
        "Матрицы: ранг",
        "Линейные пространства: базис",
        "Линейные пространства: размерность",
        "Линейные отображения",
        "Ядро и образ",
        "Евклидовы пространства",
        "Ортогональность",
        "Квадратичные формы",
        "Числовые последовательности",
        "Предел последовательности",
        "Бесконечно малые",
        "Бесконечно большие",
        "Предел функции по Коши",
        "Предел функции по Гейне",
        "Замечательные пределы",
        "Непрерывность в точке",
        "Непрерывность на отрезке",
        "Равномерная непрерывность",
        "Производная: определение по Коши",
        "Дифференцируемость",
        "Дифференциал",
        "Производные высших порядков",
        "Формула Тейлора",
        "Формула Маклорена",
        "Правило Лопиталя",
        "Интеграл Римана",
        "Интеграл Лебега",
        "Несобственные интегралы",
        "Кратные интегралы",
        "Криволинейные интегралы",
        "Поверхностные интегралы",
        "Числовые ряды: сходимость",
        "Признаки сходимости рядов",
        "Абсолютная сходимость",
        "Условная сходимость",
        "Степенные ряды",
        "Ряды Фурье",
        "ОДУ: разделение переменных",
        "ОДУ: однородные уравнения",
        "ОДУ: линейные уравнения",
        "ОДУ: уравнение Бернулли",
        "ОДУ: уравнение Риккати",
        "ОДУ второго порядка: однородные",
        "ОДУ второго порядка: неоднородные",
        "Системы ОДУ",
        "Метрические пространства",
        "Топологические пространства",
        "Нормированные пространства",
        "Банаховы пространства",
        "Гильбертовы пространства",
        "Функциональный анализ",
        "Теория меры",
        "Теория вероятностей (аксиоматика)",
        "Случайные процессы",
        "Математическая статистика"
    ]
    for idx, atype in enumerate(advanced_types):
        additional.append({"topic": atype, "grade_min": 11, "grade_max": 12, "difficulty_min": 1900+idx*15, "difficulty_max": 2400+idx*15, "category": "Высшая математика"})
    
    return additional

# Добавляем сгенерированные темы к основной базе
MATH_TOPICS_DATABASE.extend(_generate_additional_topics())

# Функция для получения тем по классу
def get_topics_by_grade(grade: int, max_topics: int = 50):
    """
    Получить темы для указанного класса
    
    Args:
        grade: Класс (1-12)
        max_topics: Максимальное количество тем
    
    Returns:
        List of topics
    """
    suitable_topics = [
        topic for topic in MATH_TOPICS_DATABASE
        if topic['grade_min'] <= grade <= topic['grade_max']
    ]
    
    # Сортируем по сложности
    suitable_topics.sort(key=lambda x: x['difficulty_min'])
    
    return suitable_topics[:max_topics]


# Функция для получения темы по сложности
def get_topic_by_difficulty(difficulty: int, grade: int = None):
    """
    Получить подходящую тему по уровню сложности
    
    Args:
        difficulty: Уровень сложности (0-3000)
        grade: Класс (опционально)
    
    Returns:
        Topic dict or None
    """
    import random
    
    suitable_topics = []
    
    for topic in MATH_TOPICS_DATABASE:
        # Проверяем соответствие сложности
        if topic['difficulty_min'] <= difficulty <= topic['difficulty_max']:
            # Если указан класс, проверяем его
            if grade is None or (topic['grade_min'] <= grade <= topic['grade_max']):
                suitable_topics.append(topic)
    
    if suitable_topics:
        return random.choice(suitable_topics)
    
    return None


# Функция для получения случайной темы для класса
def get_random_topic_for_grade(grade: int):
    """
    Получить случайную тему для класса
    
    Args:
        grade: Класс (1-12)
    
    Returns:
        Topic dict
    """
    import random
    
    topics = get_topics_by_grade(grade, max_topics=1000)
    
    if topics:
        return random.choice(topics)
    
    return None


# Статистика по базе тем
def get_database_stats():
    """Получить статистику по базе тем"""
    total = len(MATH_TOPICS_DATABASE)
    
    by_category = {}
    by_grade = {}
    
    for topic in MATH_TOPICS_DATABASE:
        # По категориям
        cat = topic['category']
        by_category[cat] = by_category.get(cat, 0) + 1
        
        # По классам
        for g in range(topic['grade_min'], topic['grade_max'] + 1):
            by_grade[g] = by_grade.get(g, 0) + 1
    
    return {
        'total_topics': total,
        'by_category': by_category,
        'by_grade': by_grade
    }


if __name__ == '__main__':
    # Вывод статистики
    stats = get_database_stats()
    print(f"📊 Всего тем в базе: {stats['total_topics']}")
    print(f"\n📚 По категориям:")
    for cat, count in sorted(stats['by_category'].items(), key=lambda x: -x[1]):
        print(f"  - {cat}: {count}")
    print(f"\n🎓 По классам:")
    for grade in sorted(stats['by_grade'].keys()):
        print(f"  - {grade} класс: {stats['by_grade'][grade]} тем")
