"""Claude API integration for generating command code."""
from __future__ import annotations
import logging
from typing import Optional
import anthropic

logger = logging.getLogger(__name__)

# Maximum retry attempts for Claude API
MAX_RETRIES = 3


async def generate_command_code(
    api_key: str,
    command_name: str,
    command_description: str,
    model: str = "claude-sonnet-4-5-20250929"
) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Generate command code using Claude API.

    Returns:
        tuple: (command_code, test_code, error_message)
               - command_code: Generated Python code for the command
               - test_code: Generated test code for the command
               - error_message: Error message if generation failed, None otherwise
    """
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are helping to generate a Matrix bot command. Generate Python code for a command with the following details:

Command name: {command_name}
Description: {command_description}

Requirements:
1. Create a single async function that matches this signature: `async def {command_name}_handler(body: str) -> Optional[str]`
2. The function should parse the command from `body` (the full message text)
3. Return a string response to send back to the user, or None if no response needed
4. Keep responses under 4000 characters
5. Include the @command decorator with appropriate pattern
6. The pattern should match `!{command_name}` followed by any arguments
7. Include clear docstring explaining what the command does

IMPORTANT:
- Import `from typing import Optional` and `from bot.commands import command`
- Use regex pattern like `r"^!{command_name}\\s*(.*)$"` to capture arguments
- Handle edge cases gracefully with error messages
- Keep the code simple and focused

Example structure:
```python
from __future__ import annotations
from typing import Optional
from . import command

@command(
    name="{command_name}",
    description="{command_description}",
    pattern=r"^!{command_name}\\s*(.*)$"
)
async def {command_name}_handler(body: str) -> Optional[str]:
    \"\"\"Your docstring here.\"\"\"
    # Your implementation here
    return "Your response"
```

Generate ONLY the Python code, no explanations or markdown. The code should be ready to save to a .py file."""

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Generating code for command '{command_name}' (attempt {attempt + 1}/{MAX_RETRIES})")

            response = client.messages.create(
                model=model,
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            command_code = response.content[0].text.strip()

            # Remove markdown code blocks if present
            if command_code.startswith("```python"):
                command_code = command_code[9:]
            if command_code.startswith("```"):
                command_code = command_code[3:]
            if command_code.endswith("```"):
                command_code = command_code[:-3]
            command_code = command_code.strip()

            # Generate test code
            test_code = await _generate_test_code(client, model, command_name, command_code, command_description)

            logger.info(f"Successfully generated code for command '{command_name}'")
            return command_code, test_code, None

        except anthropic.APIError as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt == MAX_RETRIES - 1:
                error_msg = f"Failed to generate code after {MAX_RETRIES} attempts: {e}"
                logger.error(error_msg)
                return None, None, error_msg
        except Exception as e:
            logger.exception(f"Unexpected error generating code: {e}")
            return None, None, f"Unexpected error: {e}"

    return None, None, "Failed to generate code (should not reach here)"


async def _generate_test_code(
    client: anthropic.Anthropic,
    model: str,
    command_name: str,
    command_code: str,
    description: str
) -> Optional[str]:
    """Generate test code for a command."""
    test_prompt = f"""Generate pytest test code for this Matrix bot command:

Command name: {command_name}
Description: {description}

Command code:
```python
{command_code}
```

Requirements:
1. Create async tests using pytest-asyncio
2. Test the happy path (successful execution)
3. Test edge cases (empty input, invalid input, etc.)
4. Import: `import pytest` and any needed types
5. Test function names should be descriptive (e.g., `test_{command_name}_success`)
6. Each test should call the handler function and assert the response

Generate ONLY the Python test code, no explanations or markdown."""

    try:
        response = client.messages.create(
            model=model,
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": test_prompt
            }]
        )

        test_code = response.content[0].text.strip()

        # Remove markdown code blocks if present
        if test_code.startswith("```python"):
            test_code = test_code[9:]
        if test_code.startswith("```"):
            test_code = test_code[3:]
        if test_code.endswith("```"):
            test_code = test_code[:-3]

        return test_code.strip()

    except Exception as e:
        logger.warning(f"Failed to generate test code: {e}")
        # Return a basic test template
        return f"""import pytest
from bot.commands.{command_name} import {command_name}_handler


@pytest.mark.asyncio
async def test_{command_name}_basic():
    \"\"\"Basic test for {command_name} command.\"\"\"
    result = await {command_name}_handler("!{command_name} test")
    assert result is not None
"""
