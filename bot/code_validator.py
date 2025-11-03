"""Code validation and safety checks for generated commands."""
from __future__ import annotations
import ast
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Dangerous imports/modules that should not be used
DANGEROUS_MODULES = {
    'os.system', 'subprocess', 'eval', 'exec', '__import__',
    'builtins.open', 'open',  # File operations could be dangerous
}

# Allowed safe modules
SAFE_MODULES = {
    'typing', 'bot.commands', 're', 'json', 'math', 'datetime',
    'random', 'string', 'collections', 'itertools', 'functools',
    'asyncio', 'logging'
}


class CodeValidator:
    """Validates generated code for safety and correctness."""

    def __init__(self, allow_dangerous: bool = False):
        self.allow_dangerous = allow_dangerous

    def validate(self, code: str, command_name: str) -> tuple[bool, Optional[str]]:
        """
        Validate code for safety and correctness.

        Returns:
            tuple: (is_valid, error_message)
                   - is_valid: True if code passes all checks
                   - error_message: Error description if validation fails, None otherwise
        """
        # Step 1: Try to parse the code
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error in generated code: {e}"

        # Step 2: Check for dangerous operations
        if not self.allow_dangerous:
            danger_check = self._check_dangerous_operations(tree)
            if danger_check:
                return False, danger_check

        # Step 3: Check for required structure
        structure_check = self._check_structure(tree, command_name)
        if structure_check:
            return False, structure_check

        # Step 4: Try to compile the code
        try:
            compile(code, f"<command_{command_name}>", "exec")
        except Exception as e:
            return False, f"Failed to compile code: {e}"

        return True, None

    def _check_dangerous_operations(self, tree: ast.AST) -> Optional[str]:
        """Check for dangerous operations in the AST."""
        for node in ast.walk(tree):
            # Check for dangerous function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in DANGEROUS_MODULES:
                        return f"Dangerous function call detected: {node.func.id}"

            # Check for dangerous imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in DANGEROUS_MODULES:
                        return f"Dangerous import detected: {alias.name}"

            if isinstance(node, ast.ImportFrom):
                if node.module and node.module in DANGEROUS_MODULES:
                    return f"Dangerous import detected: {node.module}"

        return None

    def _check_structure(self, tree: ast.AST, command_name: str) -> Optional[str]:
        """Check that code has the required structure."""
        # Look for the handler function
        handler_name = f"{command_name}_handler"
        found_handler = False
        found_decorator = False

        for node in ast.walk(tree):
            # Check for both async and regular function definitions
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == handler_name:
                    found_handler = True
                    # Check if it's async
                    if not isinstance(node, ast.AsyncFunctionDef):
                        return f"Handler function '{handler_name}' must be async"

                    # Check for @command decorator
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Name) and decorator.func.id == "command":
                                found_decorator = True
                        elif isinstance(decorator, ast.Name) and decorator.name == "command":
                            found_decorator = True

        if not found_handler:
            return f"Handler function '{handler_name}' not found in generated code"

        if not found_decorator:
            return f"Handler function '{handler_name}' must have @command decorator"

        return None


def validate_command_code(code: str, command_name: str) -> tuple[bool, Optional[str]]:
    """
    Convenience function to validate command code.

    Returns:
        tuple: (is_valid, error_message)
    """
    validator = CodeValidator(allow_dangerous=False)
    return validator.validate(code, command_name)


def validate_test_code(code: str) -> tuple[bool, Optional[str]]:
    """
    Validate test code for basic syntax.

    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        ast.parse(code)
    except SyntaxError as e:
        return False, f"Syntax error in test code: {e}"

    try:
        compile(code, "<test>", "exec")
    except Exception as e:
        return False, f"Failed to compile test code: {e}"

    return True, None
