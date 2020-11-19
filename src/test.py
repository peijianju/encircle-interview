import unittest
import sys
from sExpressionCalculator import evalExpression
from sExpressionCalculator import argumentScan
from sExpressionCalculator import add
from sExpressionCalculator import multiply

class Test_sExpressionCalculator(unittest.TestCase):

  def test_argumentScan(self):
    self.assertEqual(argumentScan("1 2 3"), ["1", "2", "3"])
    self.assertEqual(argumentScan("a b 3"), ["a", "b", "3"])
    self.assertEqual(argumentScan("1 (add 1 2) 3"), ["1", "(add 1 2)", "3"])
    self.assertEqual(argumentScan("1 (add 1 2) 2345 (multiply 1 2) 37"), ["1", "(add 1 2)", "2345","(multiply 1 2)", "37"])
    self.assertEqual(argumentScan("1 (((add 1 2))) ((multiply 1 2)) 3 "), ["1", "(((add 1 2)))", "((multiply 1 2))", "3"])
    self.assertEqual(argumentScan("1 (add 1 2) 2345 (add 1 (multiply 1 2) ) 37"), ["1", "(add 1 2)", "2345","(add 1 (multiply 1 2) )", "37"])
    self.assertRaises(Exception, argumentScan, ")3)")
    self.assertRaises(Exception, argumentScan, "1 (((add 1 2))")

  def test_evalExpression(self):
    self.assertNotEqual(evalExpression("1"), 3)
    self.assertEqual(evalExpression("3"), 3)
    self.assertRaises(Exception, evalExpression, "3()")
    self.assertRaises(Exception, evalExpression, "()3")
    self.assertRaises(Exception, evalExpression, "(3)")
    self.assertEqual(evalExpression("(add 1 2)"), 3)
    self.assertEqual(evalExpression("(multiply (add 1 2) (multiply 2 3) 9)"), 162)
    self.assertEqual(evalExpression("( add 1 123 (add 1 2) 2 )"), 129)

  def test_add(self):
    self.assertEqual(add("1"),1)
    self.assertEqual(add("1 2"),3)
    self.assertEqual(add("1 2 (add 3 4)"), 10)
    self.assertEqual(add("1 2 (add 3 4) (add 5 6)"), 21)
    self.assertEqual(add("1 2 (add 3 (multiply 5 6))"), 36)

    self.assertNotEqual(add("1 2 (add 3 4) (add 5 6)"), 10)


  def test_multiply(self):
    self.assertEqual(multiply("10"),10)
    self.assertEqual(multiply("10 2"), 20)
    self.assertEqual(multiply("10 2 (multiply 3 4)"), 240)
    self.assertEqual(multiply("10 20 (multiply 3 4) (multiply 5 6)"), 72000)
    self.assertEqual(multiply("10 2 (multiply 3 (multiply 5 6))"), 1800)

    self.assertNotEqual(multiply("10 2 (multiply 3 4) (multiply 5 6)"), 1234)

if __name__ == '__main__':
    unittest.main()