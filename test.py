import random
from typing import Callable
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
            calc.clear_on_next_input = bool(random.randint(0, 1))
        
        for case in cases:
            with self.subTest(f"clears {case} and all booleans",
                              case=case):
                calc = Calcuator()
                calc.buffer = case
                randomSetHasDecimal()
                randomSetNegative()
                randomSetHasPut()
                
                calc.clear()
                
                self.assertEqual(calc.buffer, "")
                self.assertFalse(calc.negative)
                self.assertFalse(calc.has_decimal)    
                self.assertFalse(calc.clear_on_next_input)            
    
    
    def testInsertNumberChar(self):
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
                    calc.add_number_character(number)
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
                    calc.add_number_character(number)
                calc.add_decimal()
                for number in second:
                    calc.add_number_character(number)
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
                self.assertEqual(calc.retrieve_number(), expected)
                
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
                self.assertTrue(calc.clear_on_next_input)
    
    
    def testAddThings_whenAlreadyPutNumber(self):
        with self.subTest("addNumber"):
            calc = Calcuator()
            calc.buffer = "PUT"
            calc.clear_on_next_input = True 
            calc.add_number_character("3")
            self.assertEqual(calc.buffer, "3")
            self.assertFalse(calc.clear_on_next_input)
            
        with self.subTest("addDecimal"):
            calc = Calcuator()
            calc.buffer = "PUT"
            calc.clear_on_next_input = True 
            calc.add_decimal()
            self.assertEqual(calc.buffer, ".")
            self.assertFalse(calc.clear_on_next_input)
            
        with self.subTest("toggleNegative"):
            calc = Calcuator()
            calc.buffer = "PUT"
            calc.clear_on_next_input = True 
            calc.toggle_negative()
            self.assertEqual(calc.buffer, "")
            self.assertTrue(calc.negative)
            self.assertFalse(calc.clear_on_next_input)
    
    
    def testSquareRoot(self):
        cases = [
            ("4", False, "2"),
            ("0", False, "0"),
            ("1", True, "Error")
        ]
        
        for num, neg, expected in cases:
            with self.subTest(f"Test sqrt works on {'-' if neg else ''}{num}",
                              num=num, neg=neg, expected=expected):
                calc = Calcuator()
                calc.buffer = num
                calc.negative = neg
                calc.do_square_root()
                self.assertEqual(calc.buffer, expected)
                self.assertTrue(calc.clear_on_next_input)
    
    
    def testAddOp(self):
        cases = [
            ("122", "1334"),
            ("199", "-2441"),
            ("33.23", "9.31542435")
        ]
        
        for n1, n2 in cases:
            with self.subTest(f"Add op {n1} + {n2}"):
                calc = Calcuator()
                test_operator(self, calc, calc.do_add, lambda x, y: x + y, n1, n2)
                
    
    def testSubtractOp(self):
        cases = [
            ("122", "1334"),
            ("199", "-2441"),
            ("33.23", "9.31542435")
        ]
        
        for n1, n2 in cases:
            with self.subTest(f"Sub op {n1} - {n2}"):
                calc = Calcuator()
                test_operator(self, calc, calc.do_subtract, lambda x, y: x - y, n1, n2)
                
                
    def testMultOp(self):
        cases = [
            ("122", "1334"),
            ("199", "-2441"),
            ("33.23", "9.31542435")
        ]
        
        for n1, n2 in cases:
            with self.subTest(f"Sub op {n1} - {n2}"):
                calc = Calcuator()
                test_operator(self, calc, calc.do_multiply, lambda x, y: x * y, n1, n2)
                
    
    def testDivOp(self):
        cases = [
            ("122", "1334"),
            ("199", "-2441"),
            ("33.23", "9.31542435")
        ]
        
        for n1, n2 in cases:
            with self.subTest(f"Sub op {n1} - {n2}"):
                calc = Calcuator()
                test_operator(self, calc, calc.do_divide, lambda x, y: x / y, n1, n2)
                
                
    def testPowerOp(self):
        cases = [
            ("6", "3"),
            ("4", "-4"),
            ("13.23", "2.31542435")
        ]
        
        for n1, n2 in cases:
            with self.subTest(f"Sub op {n1} - {n2}"):
                calc = Calcuator()
                test_operator(self, calc, calc.do_power, lambda x, y: x ** y, n1, n2)
    
    
    def testExceptionalCases(self):
        calc = Calcuator()
        cases = [
            ("2", "0", calc.do_divide),
            ("99", "999", calc.do_power)
        ]
        
        for n1, n2, op in cases:
            with self.subTest("Exception cases",
                              n1=n1, n2=n2, op=op):
                addToCalc(calc, n1)
                op()
                addToCalc(calc, n2)
                
                calc.do_equals()
                
                self.assertEqual(calc.buffer, "Error")
                
                calc.clear()
                
    
def addToCalc(calc:Calcuator, num:str):
    if num[0] == "-":
        calc.toggle_negative()
        num = num[1:]
    for n in num:
        calc.add_number_character(n)
        
        
def assertEqualNegative(tester:CalculatorTest, buffer:str, num:str):
    if num[0] == "-":
        tester.assertEqual(buffer, num[1:])
    else:
        tester.assertEqual(buffer, num)
    
    
def test_operator(tester:CalculatorTest, calc:Calcuator, tested_op:Callable[[], None], intended_op:Callable[[float, float], float], n1:str, n2:str):
    
    n1num = float(n1)
    n2num = float(n2)
    
    addToCalc(calc, n1)
        
    assertEqualNegative(tester, calc.buffer, n1)
    
    tested_op()
    
    tester.assertEqual(calc.last_number, n1num)
    tester.assertEqual(calc.buffer, "")
    tester.assertEqual(calc.binary_operation(3, 7), intended_op(3, 7)) 
    
    addToCalc(calc, n2)
        
    assertEqualNegative(tester, calc.buffer, n2)
    
    calc.do_equals()
    
    tester.assertEqual(calc.last_number, 0)
    tester.assertAlmostEqual(float(calc.buffer) * (-1 if calc.negative else 1), intended_op(n1num, n2num))
    tester.assertTrue(calc.clear_on_next_input)
    
    
def main():
    unittest.main()


if __name__ == "__main__":
    main()
    