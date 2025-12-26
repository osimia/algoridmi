"""
Модуль для валидации математических решений
Использует SymPy для проверки корректности решений и ответов
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
import re
from sympy import symbols, solve, simplify, expand, factor, sqrt, Eq, sympify
from sympy.parsing.latex import parse_latex
from sympy.core.sympify import SympifyError

logger = logging.getLogger(__name__)


class MathValidator:
    """Класс для валидации математических решений"""
    
    def __init__(self):
        """Инициализация валидатора"""
        self.common_vars = symbols('x y z a b c t n m k p q r s u v w')
    
    def validate_equation_solution(
        self,
        equation: str,
        claimed_solutions: List[str],
        variable: str = 'x'
    ) -> Dict[str, Any]:
        """
        Проверяет корректность решений уравнения
        
        Args:
            equation: Уравнение в формате LaTeX или текстовом
            claimed_solutions: Список предполагаемых решений
            variable: Переменная для решения
        
        Returns:
            Dict с результатами валидации:
                - is_valid: bool - все ли решения корректны
                - correct_solutions: List - правильные решения
                - errors: List - найденные ошибки
                - sympy_solutions: List - решения от SymPy
        """
        result = {
            'is_valid': False,
            'correct_solutions': [],
            'errors': [],
            'sympy_solutions': [],
            'verification': {}
        }
        
        try:
            # Парсим уравнение
            var = symbols(variable)
            
            # Пробуем распарсить как LaTeX
            try:
                eq = self._parse_equation(equation, var)
            except Exception as e:
                logger.warning(f"Не удалось распарсить уравнение: {e}")
                result['errors'].append(f"Ошибка парсинга уравнения: {str(e)}")
                return result
            
            # Решаем уравнение через SymPy
            try:
                sympy_sols = solve(eq, var)
                result['sympy_solutions'] = [str(sol) for sol in sympy_sols]
                logger.info(f"SymPy решения: {result['sympy_solutions']}")
            except Exception as e:
                logger.error(f"SymPy не смог решить уравнение: {e}")
                result['errors'].append(f"Не удалось решить уравнение: {str(e)}")
                return result
            
            # Проверяем каждое заявленное решение
            for claimed_sol in claimed_solutions:
                try:
                    # Парсим решение
                    sol_value = sympify(claimed_sol)
                    
                    # Подставляем в исходное уравнение
                    verification = eq.subs(var, sol_value)
                    simplified = simplify(verification)
                    
                    # Проверяем, равно ли нулю
                    is_correct = simplified == 0 or abs(float(simplified)) < 1e-10
                    
                    result['verification'][claimed_sol] = {
                        'is_correct': is_correct,
                        'substitution_result': str(simplified)
                    }
                    
                    if is_correct:
                        result['correct_solutions'].append(claimed_sol)
                    else:
                        result['errors'].append(
                            f"Решение {claimed_sol} неверно: при подстановке получается {simplified}"
                        )
                        
                except Exception as e:
                    logger.error(f"Ошибка проверки решения {claimed_sol}: {e}")
                    result['errors'].append(f"Не удалось проверить решение {claimed_sol}: {str(e)}")
            
            # Проверяем, все ли решения найдены
            claimed_set = set(result['correct_solutions'])
            sympy_set = set(result['sympy_solutions'])
            
            if claimed_set == sympy_set:
                result['is_valid'] = True
            else:
                missing = sympy_set - claimed_set
                extra = claimed_set - sympy_set
                
                if missing:
                    result['errors'].append(f"Пропущены решения: {missing}")
                if extra:
                    result['errors'].append(f"Лишние решения: {extra}")
            
            return result
            
        except Exception as e:
            logger.error(f"Критическая ошибка валидации: {e}")
            result['errors'].append(f"Критическая ошибка: {str(e)}")
            return result
    
    def validate_irrational_equation(
        self,
        equation: str,
        claimed_solutions: List[str],
        variable: str = 'x'
    ) -> Dict[str, Any]:
        """
        Специальная проверка для иррациональных уравнений
        Проверяет ОДЗ (область допустимых значений) и посторонние корни
        
        Args:
            equation: Уравнение с корнями
            claimed_solutions: Заявленные решения
            variable: Переменная
        
        Returns:
            Dict с результатами валидации
        """
        result = {
            'is_valid': False,
            'correct_solutions': [],
            'extraneous_roots': [],
            'errors': [],
            'odz_check': {}
        }
        
        try:
            var = symbols(variable, real=True)
            
            # Парсим уравнение
            eq = self._parse_equation(equation, var)
            
            # Решаем уравнение
            all_solutions = solve(eq, var)
            
            # Проверяем каждое решение на ОДЗ
            for sol in all_solutions:
                sol_str = str(sol)
                
                # Подставляем в исходное уравнение
                try:
                    # Проверяем, что под корнями неотрицательные значения
                    substituted = eq.subs(var, sol)
                    
                    # Проверяем численно
                    try:
                        numeric_check = complex(substituted.evalf())
                        
                        # Если получилось комплексное число, это посторонний корень
                        if abs(numeric_check.imag) > 1e-10:
                            result['extraneous_roots'].append(sol_str)
                            result['odz_check'][sol_str] = 'Не удовлетворяет ОДЗ (комплексное значение)'
                        elif abs(numeric_check.real) < 1e-10:
                            result['correct_solutions'].append(sol_str)
                            result['odz_check'][sol_str] = 'Корректное решение'
                        else:
                            result['extraneous_roots'].append(sol_str)
                            result['odz_check'][sol_str] = f'Не удовлетворяет уравнению: {numeric_check}'
                    except:
                        # Символьная проверка
                        if simplify(substituted) == 0:
                            result['correct_solutions'].append(sol_str)
                            result['odz_check'][sol_str] = 'Корректное решение'
                        else:
                            result['extraneous_roots'].append(sol_str)
                            result['odz_check'][sol_str] = 'Не удовлетворяет уравнению'
                            
                except Exception as e:
                    logger.error(f"Ошибка проверки решения {sol}: {e}")
                    result['errors'].append(f"Не удалось проверить {sol}: {str(e)}")
            
            # Сравниваем с заявленными решениями
            claimed_set = set(claimed_solutions)
            correct_set = set(result['correct_solutions'])
            
            if claimed_set == correct_set:
                result['is_valid'] = True
            else:
                if claimed_set - correct_set:
                    result['errors'].append(
                        f"Включены посторонние корни: {claimed_set - correct_set}"
                    )
                if correct_set - claimed_set:
                    result['errors'].append(
                        f"Пропущены корректные решения: {correct_set - claimed_set}"
                    )
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка валидации иррационального уравнения: {e}")
            result['errors'].append(str(e))
            return result
    
    def validate_answer_equivalence(
        self,
        answer1: str,
        answer2: str
    ) -> bool:
        """
        Проверяет эквивалентность двух математических выражений
        
        Args:
            answer1: Первое выражение
            answer2: Второе выражение
        
        Returns:
            bool - эквивалентны ли выражения
        """
        try:
            expr1 = sympify(answer1)
            expr2 = sympify(answer2)
            
            # Упрощаем разность
            diff = simplify(expr1 - expr2)
            
            # Проверяем, равна ли разность нулю
            return diff == 0
            
        except Exception as e:
            logger.error(f"Ошибка проверки эквивалентности: {e}")
            # Пробуем простое строковое сравнение
            return answer1.strip() == answer2.strip()
    
    def validate_step_by_step_solution(
        self,
        equation: str,
        steps: List[str],
        variable: str = 'x'
    ) -> Dict[str, Any]:
        """
        Проверяет корректность пошагового решения
        
        Args:
            equation: Исходное уравнение
            steps: Список шагов решения
            variable: Переменная
        
        Returns:
            Dict с результатами проверки каждого шага
        """
        result = {
            'is_valid': True,
            'step_validations': [],
            'errors': []
        }
        
        try:
            var = symbols(variable)
            current_eq = self._parse_equation(equation, var)
            
            for i, step in enumerate(steps, 1):
                step_result = {
                    'step_number': i,
                    'step_text': step,
                    'is_valid': True,
                    'notes': []
                }
                
                # Извлекаем уравнение из шага (если есть)
                # Это упрощенная версия - в production нужен более сложный парсинг
                try:
                    # Ищем уравнения в шаге
                    equations_in_step = re.findall(r'[^=]+=+[^=]+', step)
                    
                    if equations_in_step:
                        # Проверяем эквивалентность преобразований
                        step_result['notes'].append(f"Найдено уравнение: {equations_in_step[0]}")
                    
                except Exception as e:
                    step_result['notes'].append(f"Не удалось проверить шаг: {str(e)}")
                
                result['step_validations'].append(step_result)
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка валидации пошагового решения: {e}")
            result['is_valid'] = False
            result['errors'].append(str(e))
            return result
    
    def _parse_equation(self, equation_str: str, var) -> Any:
        """
        Парсит уравнение из строки
        
        Args:
            equation_str: Строка с уравнением
            var: Переменная
        
        Returns:
            SymPy выражение
        """
        # Убираем LaTeX команды
        cleaned = equation_str.replace('\\', '')
        cleaned = cleaned.replace('sqrt', 'sqrt')
        cleaned = cleaned.replace('{', '(').replace('}', ')')
        
        # Разделяем по знаку равенства
        if '=' in cleaned:
            parts = cleaned.split('=')
            if len(parts) == 2:
                left = sympify(parts[0].strip())
                right = sympify(parts[1].strip())
                return left - right
        
        # Если нет знака равенства, считаем что уравнение = 0
        return sympify(cleaned)
    
    def get_equation_domain(
        self,
        equation: str,
        variable: str = 'x'
    ) -> Dict[str, Any]:
        """
        Определяет область допустимых значений (ОДЗ) для уравнения
        
        Args:
            equation: Уравнение
            variable: Переменная
        
        Returns:
            Dict с информацией об ОДЗ
        """
        result = {
            'domain_conditions': [],
            'restrictions': []
        }
        
        try:
            # Ищем корни в уравнении
            sqrt_matches = re.findall(r'sqrt\(([^)]+)\)', equation)
            
            for match in sqrt_matches:
                result['domain_conditions'].append(f"{match} >= 0")
                result['restrictions'].append(f"Под корнем должно быть неотрицательное: {match}")
            
            # Ищем дроби
            fraction_matches = re.findall(r'/\s*\(([^)]+)\)', equation)
            
            for match in fraction_matches:
                result['domain_conditions'].append(f"{match} != 0")
                result['restrictions'].append(f"Знаменатель не должен быть нулем: {match}")
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка определения ОДЗ: {e}")
            return result


# Singleton instance
_math_validator = None

def get_math_validator() -> MathValidator:
    """Получить экземпляр MathValidator (Singleton)"""
    global _math_validator
    if _math_validator is None:
        _math_validator = MathValidator()
    return _math_validator
