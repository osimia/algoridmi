"""
Unit-тесты для модуля валидации математических решений
"""

import unittest
from core.math_validator import MathValidator


class TestMathValidator(unittest.TestCase):
    """Тесты для MathValidator"""
    
    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.validator = MathValidator()
    
    def test_simple_linear_equation(self):
        """Тест простого линейного уравнения"""
        equation = "x + 5 = 12"
        solutions = ["7"]
        
        result = self.validator.validate_equation_solution(equation, solutions)
        
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['correct_solutions'], ["7"])
        self.assertEqual(len(result['errors']), 0)
    
    def test_quadratic_equation(self):
        """Тест квадратного уравнения"""
        equation = "x^2 - 5*x + 6 = 0"
        solutions = ["2", "3"]
        
        result = self.validator.validate_equation_solution(equation, solutions)
        
        self.assertTrue(result['is_valid'])
        self.assertEqual(set(result['correct_solutions']), {"2", "3"})
    
    def test_irrational_equation_correct(self):
        """Тест иррационального уравнения с корректным решением"""
        # sqrt(x+5) = x-1 имеет решение x=4
        equation = "sqrt(x+5) = x-1"
        solutions = ["4"]
        
        result = self.validator.validate_irrational_equation(equation, solutions)
        
        self.assertTrue(result['is_valid'])
        self.assertIn("4", result['correct_solutions'])
        # x=-1 должен быть посторонним корнем
        self.assertNotIn("-1", result['correct_solutions'])
    
    def test_irrational_equation_extraneous_root(self):
        """Тест обнаружения постороннего корня"""
        equation = "sqrt(x+5) = x-1"
        # -1 является посторонним корнем
        solutions = ["-1", "4"]
        
        result = self.validator.validate_irrational_equation(equation, solutions)
        
        # Должен быть только один корректный корень
        self.assertEqual(len(result['correct_solutions']), 1)
        self.assertIn("4", result['correct_solutions'])
        self.assertIn("-1", result['extraneous_roots'])
    
    def test_answer_equivalence(self):
        """Тест проверки эквивалентности ответов"""
        # 0.5 и 1/2 эквивалентны
        self.assertTrue(
            self.validator.validate_answer_equivalence("0.5", "1/2")
        )
        
        # 2*x и x*2 эквивалентны
        self.assertTrue(
            self.validator.validate_answer_equivalence("2*x", "x*2")
        )
        
        # 3 и 4 не эквивалентны
        self.assertFalse(
            self.validator.validate_answer_equivalence("3", "4")
        )
    
    def test_domain_detection(self):
        """Тест определения ОДЗ"""
        equation = "sqrt(x-3) + sqrt(2*x+1) = 5"
        
        result = self.validator.get_equation_domain(equation)
        
        # Должны быть найдены условия для ОДЗ
        self.assertGreater(len(result['domain_conditions']), 0)
        self.assertIn('restrictions', result)
    
    def test_wrong_solution(self):
        """Тест обнаружения неправильного решения"""
        equation = "x + 5 = 12"
        solutions = ["10"]  # Неправильный ответ
        
        result = self.validator.validate_equation_solution(equation, solutions)
        
        self.assertFalse(result['is_valid'])
        self.assertGreater(len(result['errors']), 0)
    
    def test_missing_solution(self):
        """Тест обнаружения пропущенного решения"""
        equation = "x^2 - 5*x + 6 = 0"
        solutions = ["2"]  # Пропущено решение x=3
        
        result = self.validator.validate_equation_solution(equation, solutions)
        
        self.assertFalse(result['is_valid'])
        self.assertIn("Пропущены решения", str(result['errors']))


class TestIrrationalEquations(unittest.TestCase):
    """Специальные тесты для иррациональных уравнений"""
    
    def setUp(self):
        self.validator = MathValidator()
    
    def test_sqrt_equation_1(self):
        """sqrt(x+5) = x-1"""
        equation = "sqrt(x+5) = x-1"
        
        result = self.validator.validate_irrational_equation(equation, ["4"])
        
        self.assertTrue(result['is_valid'])
        self.assertNotIn("-1", result['correct_solutions'])
    
    def test_sqrt_equation_2(self):
        """sqrt(2*x+3) = x"""
        equation = "sqrt(2*x+3) = x"
        
        result = self.validator.validate_irrational_equation(equation, ["3"])
        
        # x=3 корректное решение
        self.assertIn("3", result['correct_solutions'])
        # x=-1 посторонний корень
        self.assertNotIn("-1", result['correct_solutions'])


if __name__ == '__main__':
    unittest.main()
