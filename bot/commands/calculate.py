from __future__ import annotations
from typing import Optional
import re
from . import command


@command(
    name="calculate",
    description="Calculate the result of the simple calculation given e.g. 3+4 or 5-5 or 7*7. Do not use eval.",
    pattern=r"^!calculate\s*(.*)$"
)
async def calculate_handler(body: str) -> Optional[str]:
    """
    Calculate the result of a simple mathematical expression.
    
    Supports basic operations: addition (+), subtraction (-), multiplication (*), and division (/).
    Does not use eval() for security reasons.
    
    Args:
        body: The full message text containing the command and expression
        
    Returns:
        The calculation result as a string, or an error message if the expression is invalid
    """
    match = re.match(r"^!calculate\s*(.*)$", body.strip())
    if not match:
        return "Usage: !calculate <expression>\nExample: !calculate 3+4"
    
    expression = match.group(1).strip()
    
    if not expression:
        return "Usage: !calculate <expression>\nExample: !calculate 3+4"
    
    # Remove all whitespace
    expression = expression.replace(" ", "")
    
    # Parse and calculate the expression
    try:
        result = parse_expression(expression)
        return f"{expression} = {result}"
    except ValueError as e:
        return f"Error: {str(e)}"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception:
        return "Error: Invalid expression. Use simple operations like: 3+4, 5-5, 7*7, 10/2"


def parse_expression(expr: str) -> float:
    """
    Parse and evaluate a simple mathematical expression without using eval().
    
    Args:
        expr: Mathematical expression string
        
    Returns:
        The calculated result
        
    Raises:
        ValueError: If the expression is invalid
        ZeroDivisionError: If division by zero is attempted
    """
    # Handle multiplication and division first (operator precedence)
    # Split by + and - while keeping track of operations
    parts = []
    current_num = ""
    operations = []
    
    i = 0
    while i < len(expr):
        char = expr[i]
        
        if char in "+-":
            if current_num or (char == "-" and not current_num and not parts):
                # Handle negative numbers at the start
                if char == "-" and not current_num and not parts:
                    current_num = "-"
                else:
                    if current_num:
                        parts.append(evaluate_mult_div(current_num))
                        current_num = ""
                    operations.append(char)
            else:
                raise ValueError("Invalid expression format")
        else:
            current_num += char
        
        i += 1
    
    if current_num:
        parts.append(evaluate_mult_div(current_num))
    
    if not parts:
        raise ValueError("No valid expression found")
    
    # Now handle addition and subtraction from left to right
    result = parts[0]
    for i, op in enumerate(operations):
        if op == "+":
            result += parts[i + 1]
        elif op == "-":
            result -= parts[i + 1]
    
    return result


def evaluate_mult_div(expr: str) -> float:
    """
    Evaluate multiplication and division in an expression.
    
    Args:
        expr: Expression containing only numbers, *, and /
        
    Returns:
        The calculated result
        
    Raises:
        ValueError: If the expression is invalid
        ZeroDivisionError: If division by zero is attempted
    """
    parts = []
    operations = []
    current_num = ""
    
    i = 0
    while i < len(expr):
        char = expr[i]
        
        if char in "*/":
            if current_num:
                try:
                    parts.append(float(current_num))
                except ValueError:
                    raise ValueError(f"Invalid number: {current_num}")
                current_num = ""
                operations.append(char)
            else:
                raise ValueError("Invalid expression format")
        else:
            current_num += char
        
        i += 1
    
    if current_num:
        try:
            parts.append(float(current_num))
        except ValueError:
            raise ValueError(f"Invalid number: {current_num}")
    
    if not parts:
        raise ValueError("No valid expression found")
    
    # Evaluate from left to right
    result = parts[0]
    for i, op in enumerate(operations):
        if op == "*":
            result *= parts[i + 1]
        elif op == "/":
            if parts[i + 1] == 0:
                raise ZeroDivisionError()
            result /= parts[i + 1]
    
    return result