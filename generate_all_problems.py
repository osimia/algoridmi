#!/usr/bin/env python
"""
Скрипт массовой генерации задач для всех классов и уровней сложности
Кросс-платформенный (работает на Windows, Linux, Mac)
"""

import subprocess
import sys
import time
from datetime import datetime


# Цвета для консоли
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_colored(text, color=Colors.ENDC):
    """Печать цветного текста"""
    print(f"{color}{text}{Colors.ENDC}")


def print_header(text):
    """Печать заголовка"""
    print_colored("=" * 50, Colors.OKCYAN)
    print_colored(text, Colors.OKGREEN)
    print_colored("=" * 50, Colors.OKCYAN)
    print()


def run_command(cmd):
    """Запуск команды и возврат результата"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print_colored(f"   ❌ Ошибка: {e}", Colors.FAIL)
        return False


def generate_for_grade(grade, count, delay):
    """Генерация задач для конкретного класса"""
    print_colored(f"📝 Класс {grade}...", Colors.WARNING)
    
    cmd = f"python manage.py generate_problems_bulk --count {count} --grade {grade} --delay {delay}"
    
    if run_command(cmd):
        print_colored(f"   ✅ Успешно сгенерировано: {count} задач", Colors.OKGREEN)
        return count, 0
    else:
        print_colored(f"   ❌ Ошибка генерации для класса {grade}", Colors.FAIL)
        return 0, count


def generate_for_difficulty(name, min_diff, max_diff, count, delay):
    """Генерация задач для уровня сложности"""
    print_colored(f"🎓 Уровень: {name} ({min_diff}-{max_diff})", Colors.WARNING)
    
    cmd = f"python manage.py generate_problems_bulk --count {count} --difficulty-min {min_diff} --difficulty-max {max_diff} --delay {delay}"
    
    if run_command(cmd):
        print_colored(f"   ✅ Успешно сгенерировано: {count} задач", Colors.OKGREEN)
        return count, 0
    else:
        print_colored(f"   ❌ Ошибка генерации для уровня {name}", Colors.FAIL)
        return 0, count


def main():
    """Основная функция"""
    start_time = datetime.now()
    
    print_header("🚀 МАССОВАЯ ГЕНЕРАЦИЯ ЗАДАЧ")
    
    # Параметры генерации
    problems_per_grade = 10
    delay = 2.0
    
    # Счетчики
    total_problems = 0
    success_count = 0
    error_count = 0
    
    print_colored("📊 Параметры генерации:", Colors.OKCYAN)
    print_colored(f"   - Задач на класс: {problems_per_grade}", Colors.ENDC)
    print_colored(f"   - Задержка: {delay} сек", Colors.ENDC)
    print()
    
    # ========================================
    # ЧАСТЬ 1: Генерация для школьных классов (1-12)
    # ========================================
    
    print_header("📚 ЧАСТЬ 1: Генерация задач для школьных классов (1-12)")
    
    for grade in range(1, 13):
        success, errors = generate_for_grade(grade, problems_per_grade, delay)
        success_count += success
        error_count += errors
        total_problems += problems_per_grade
        print()
    
    # ========================================
    # ЧАСТЬ 2: Генерация для разных уровней сложности
    # ========================================
    
    print_header("🎯 ЧАСТЬ 2: Генерация задач для разных уровней сложности")
    
    difficulty_levels = [
        {"name": "Начальный", "min": 0, "max": 300, "count": 10},
        {"name": "Легкий", "min": 300, "max": 600, "count": 10},
        {"name": "Средний", "min": 600, "max": 900, "count": 10},
        {"name": "Выше среднего", "min": 900, "max": 1200, "count": 10},
        {"name": "Сложный", "min": 1200, "max": 1500, "count": 10},
        {"name": "Очень сложный", "min": 1500, "max": 2000, "count": 10},
        {"name": "Экспертный", "min": 2000, "max": 3000, "count": 10}
    ]
    
    for level in difficulty_levels:
        success, errors = generate_for_difficulty(
            level["name"],
            level["min"],
            level["max"],
            level["count"],
            delay
        )
        success_count += success
        error_count += errors
        total_problems += level["count"]
        print()
    
    # ========================================
    # ИТОГОВАЯ СТАТИСТИКА
    # ========================================
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print()
    print_header("🎉 ГЕНЕРАЦИЯ ЗАВЕРШЕНА!")
    
    print_colored("📊 Статистика:", Colors.OKCYAN)
    print_colored(f"   - Всего задач запланировано: {total_problems}", Colors.ENDC)
    print_colored(f"   - Успешно сгенерировано: {success_count}", Colors.OKGREEN)
    print_colored(f"   - Ошибок: {error_count}", Colors.FAIL)
    print_colored(f"   - Время выполнения: {duration}", Colors.ENDC)
    print()
    
    # Проверяем общее количество задач в БД
    print_colored("📚 Проверяем БД...", Colors.OKCYAN)
    run_command('python manage.py shell -c "from problems.models import Problem; print(f\'Всего задач в БД: {Problem.objects.count()}\')"')
    
    print()
    print_header("✅ Готово!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_colored("\n⚠️  Генерация прервана пользователем", Colors.WARNING)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n❌ Критическая ошибка: {e}", Colors.FAIL)
        sys.exit(1)
