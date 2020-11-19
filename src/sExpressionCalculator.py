
# -*- coding: utf-8 -*-
"""S-expression calculator
encircle code interview: https://gist.github.com/rraval/2ef5e2ff228e022653db2055fc12ea9d
"""

import argparse

def add(argument):
  """ADD function
  Args:
    argument (str): String contains one or more s-expression, e.g. "1 2 3", "(add 1 2) 3"
  Returns:
    int: sum of the results of each s-expression in argument string
  """
  result = 0
  args = argumentScan(argument)
  for arg in args:
    result = result+evalExpression(arg)
  return result

def multiply(argument):
  """MULTIPLY function
  Args:
    argument (str): String contains one or more s-expression, e.g. "1 2 3", "(add 1 2) 3"
  Returns:
    int: multiply of the results of each s-expression in argument string
  """
  result = 1
  args = argumentScan(argument)
  for arg in args:
    result = result*evalExpression(arg)
  return result

def evalExpression(expr):
  """evalExpression function
  Args:
    expr (str): a s-expression, e.g. "1", "(add 1 2)"
  Returns:
    int: evaluation result the s-expression
  Raises:
    Exception when function is unknown
    Exception when expression not valid
  """
  expr=expr.strip()
  if expr.isdecimal():
    return int(expr)

  if not expr.startswith("(") or not expr.endswith(")"):
    raise Exception(f"\"{expr}\" is not a valid expression")
    
  expr=expr[1:-1].strip()
  function=expr.split(' ',1)[0].lower().strip()
  argument=expr.split(' ',1)[1].lower().strip()

  if function == "add":
    return add(argument)
  elif function == "multiply":
    return multiply(argument)
  else:
    raise Exception(f"\"{function}\" is an unknown function")

def argumentScan(arg):
  """argumentScan function

  Scan s-expression string, and break it into individual expression list

  Args:
    arg (str): String contains one or more s-expression, e.g. "1 2 3", "(add 1 2) 3"
  Returns:
    list: list of the s-expression, ["1", "2", "3"], ["(add 1 2)", "3"]
  Raises:
    Exception when brackets mismatched
  """
  scannedArgs=[]
  arg=" "+arg+" "
  markerAbove=0
  markerBelow=0
  openBracketCount=0
  closeBracketCount=0
  while markerBelow < len(arg):
    if arg[markerBelow] == "(":
      openBracketCount=openBracketCount+1
    if arg[markerAbove] == " ":
      markerAbove=markerBelow
    else:
      if arg[markerBelow] == ")":
        if closeBracketCount > openBracketCount: # in case of ")abc("
          raise Exception(f"\"{arg}\" has a mismatched bracket")
        closeBracketCount = closeBracketCount+1
      if arg[markerBelow] == " " and markerBelow > markerAbove:
        if arg[markerAbove] != "(":
          scannedArgs.append(arg[markerAbove:markerBelow])
          markerAbove=markerBelow
        if arg[markerAbove] == "(" and arg[markerBelow-1] == ")":
          if openBracketCount-closeBracketCount == 0: # uttermost bracket matched 
            openBracketCount=0
            closeBracketCount=0
            scannedArgs.append(arg[markerAbove:markerBelow])
            markerAbove=markerBelow
    markerBelow=markerBelow+1

  if openBracketCount-closeBracketCount != 0:
    raise Exception(f"\"{arg}\" has a mismatched bracket")
  return scannedArgs
  
if __name__ == '__main__':
  cliDescription="""S-expression calculator
  Take an S-expression and calculate and print the result
  Need python 3.8.5+ to run
  Example:
    python3 src/sExpressionCalculator.py 63
    python3 src/sExpressionCalculator.py "(add 3 6 9)"
    python3 src/sExpressionCalculator.py "(multiply 3 6 9)"
    python3 src/sExpressionCalculator.py "(multiply (add 1 2) (multiply 2 3) 9)"
  """

  expressionHelp="""Simplified S-expression.
  An expression can be in one of two forms:
  1. Positive Integers. E.g. 123
  2. Function calls. In the form of 
      (FUNCTION EXPR EXPR)
    Only add and multiply are supported. Function name is case-insensitive
    e.g. "(add 123 456)" "(multiply (add 1 2) 3)" "(multiply (ADD 1 2) (ADD 2 3) 9)"
    
  """
  parser = argparse.ArgumentParser(description=cliDescription, formatter_class=argparse.RawTextHelpFormatter)

  parser.add_argument('expression', metavar='EXPR', nargs='?',
                      help=expressionHelp)
  args = parser.parse_args()
  if args.expression is None:
    parser.print_help()
  else:
    expression=args.expression
    print(evalExpression(expression))
