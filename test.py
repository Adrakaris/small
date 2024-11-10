import random
import unittest

from main import Calcuator

class CalculatorTest(unittest.TestCase):
    
    def testClear(self):
        cases = [
            "", "3333"
        ]
        
        def randomSetHasDecimal():
            calc.has_decimal = bool(random.randint(0, 1))
            
        def randomSetNegative():
            calc.negative = bool(random.randint(0, 1))
        
        def randomSetHasPut():
            calc.has_put_number = bool(random.randint(0, 1))
        
        for case in cases:
            with self.subTest(f"clears {case} and all booleans",
                              case=case):
                calc = Calcuator()
                calc.buffer = case
                randomSetHasDecimal()
                randomSetNegative()
                
                calc.clear()
                
                self.assertEqual(calc.buffer, "")
                self.assertFalse(calc.negative)
                self.assertFalse(calc.has_decimal)    
                self.assertFalse(calc.has_put_number)            
    
    
    def testAddNumber(self):
        cases = [
            ("3", "3"),
            ("3777788", "3777788"),
            ("123456789123456", "123456789123456"[:Calcuator.max_length]),
        ]
        
        for numbers, expected in cases:
            with self.subTest(f"add adds {numbers} (removing any that overflow)",
                              numbers=numbers, expected=expected):
                calc = Calcuator()
                for number in numbers:
                    calc.add_number(number)
                self.assertEqual(calc.buffer, expected)
                                
    
    def testAddDecimal(self):
        cases = [
            ("", "", "."),
            ("", "33", ".33"),
            ("3", "3", "3.3"),
            ("33", "", "33."),
            ("123456789012", "", "123456789012"),
            ("1234567890123", "", "1234567890123"),
            ("", "1234567890123", ".123456789012"),
            ("123", "56789012345", "123.567890123")
        ]
        
        for first, second, expected in cases:
            with self.subTest(f"addDecimal between {first}, {second}",
                              first=first, second=second, expected=expected):
                calc = Calcuator()
                for number in first:
                    calc.add_number(number)
                calc.add_decimal()
                for number in second:
                    calc.add_number(number)
                self.assertEqual(calc.buffer, expected)
                if "." in expected:
                    self.assertTrue(calc.has_decimal)
    
    
    def testEvaluate(self):
        cases = [
            ("", False, 0),
            ("12345", False, 12345),
            ("37.34", False, 37.34),
            (".334", False, 0.334),
            ("45.", False, 45),
            ("12", True, -12),
            ("3.3", True, -3.3)
        ]
        
        for text, negative, expected in cases:
            with self.subTest(f"evaluate evals {text} correctly", 
                              text=text, negative=negative, expected=expected):
                calc = Calcuator()
                calc.buffer = text
                calc.negative = negative
                self.assertEqual(calc.evaluate(), expected)
                
    def testPutNumber(self):
        cases = [
            (0, "0"),
            (14, "14"),
            (123456789012345, "1.23456789e14"),
            (22111222211112222, "2.21112222e16"),
            (1e100, "1e100"),
            (1.7976931348623157e+308, "1.7976931e308"),
            (0.3, "0.3"),
            (33.3, "33.3"),
            (1234567.1234567, "1234567.12345"),
            (0.12345671234567, "0.12345671234"),
            (0, "0"),
            (-14, "14"),
            (-123456789012345, "1.23456789e14"),
            (-1e100, "1e100"),
            (-1.7976931348623157e+308, "1.7976931e308"),
            (-0.3, "0.3"),
            (-33.3, "33.3"),
            (-1234567.1234567, "1234567.12345"),
            (-0.12345671234567, "0.12345671234")
        ]
        
        for num, expected in cases:
            with self.subTest(f"putNumber puts {num} correctly",
                              num=num, expected=expected):
                calc = Calcuator()
                calc.put_number(num)
                self.assertEqual(calc.buffer, expected)
                if num < 0:
                    self.assertTrue(calc.negative)
                self.assertTrue(calc.has_put_number)
    
    
    def testAddThings_whenAlreadyPutNumber(self):
        with self.subTest("addNumber"):
            calc = Calcuator()
            calc.buffer = "PUT"
            calc.has_put_number = True 
            calc.add_number("3")
            self.assertEqual(calc.buffer, "3")
            self.assertFalse(calc.has_put_number)
            
        with self.subTest("addDecimal"):
            calc = Calcuator()
            calc.buffer = "PUT"
            calc.has_put_number = True 
            calc.add_decimal()
            self.assertEqual(calc.buffer, ".")
            self.assertFalse(calc.has_put_number)
            
        with self.subTest("toggleNegative"):
            calc = Calcuator()
            calc.buffer = "PUT"
            calc.has_put_number = True 
            calc.toggle_negative()
            self.assertEqual(calc.buffer, "")
            self.assertTrue(calc.negative)
            self.assertFalse(calc.has_put_number)
    
    
def main():
    unittest.main()


if __name__ == "__main__":
    main()
    