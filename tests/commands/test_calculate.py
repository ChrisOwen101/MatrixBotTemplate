import pytest
from typing import Optional


@pytest.mark.asyncio
async def test_calculate_addition():
    from . import calculate_handler
    result = await calculate_handler("!calculate 3+4")
    assert result == "3+4 = 7.0"


@pytest.mark.asyncio
async def test_calculate_subtraction():
    from . import calculate_handler
    result = await calculate_handler("!calculate 5-5")
    assert result == "5-5 = 0.0"


@pytest.mark.asyncio
async def test_calculate_multiplication():
    from . import calculate_handler
    result = await calculate_handler("!calculate 7*7")
    assert result == "7*7 = 49.0"


@pytest.mark.asyncio
async def test_calculate_division():
    from . import calculate_handler
    result = await calculate_handler("!calculate 10/2")
    assert result == "10/2 = 5.0"


@pytest.mark.asyncio
async def test_calculate_with_spaces():
    from . import calculate_handler
    result = await calculate_handler("!calculate 3 + 4")
    assert result == "3+4 = 7.0"


@pytest.mark.asyncio
async def test_calculate_complex_expression():
    from . import calculate_handler
    result = await calculate_handler("!calculate 2+3*4")
    assert result == "2+3*4 = 14.0"


@pytest.mark.asyncio
async def test_calculate_with_operator_precedence():
    from . import calculate_handler
    result = await calculate_handler("!calculate 10-2*3")
    assert result == "10-2*3 = 4.0"


@pytest.mark.asyncio
async def test_calculate_division_and_multiplication():
    from . import calculate_handler
    result = await calculate_handler("!calculate 12/3*2")
    assert result == "12/3*2 = 8.0"


@pytest.mark.asyncio
async def test_calculate_negative_number():
    from . import calculate_handler
    result = await calculate_handler("!calculate -5+3")
    assert result == "-5+3 = -2.0"


@pytest.mark.asyncio
async def test_calculate_floating_point():
    from . import calculate_handler
    result = await calculate_handler("!calculate 5.5+2.5")
    assert result == "5.5+2.5 = 8.0"


@pytest.mark.asyncio
async def test_calculate_empty_expression():
    from . import calculate_handler
    result = await calculate_handler("!calculate")
    assert result == "Usage: !calculate <expression>\nExample: !calculate 3+4"


@pytest.mark.asyncio
async def test_calculate_empty_expression_with_spaces():
    from . import calculate_handler
    result = await calculate_handler("!calculate   ")
    assert result == "Usage: !calculate <expression>\nExample: !calculate 3+4"


@pytest.mark.asyncio
async def test_calculate_division_by_zero():
    from . import calculate_handler
    result = await calculate_handler("!calculate 5/0")
    assert result == "Error: Division by zero"


@pytest.mark.asyncio
async def test_calculate_invalid_characters():
    from . import calculate_handler
    result = await calculate_handler("!calculate 3+abc")
    assert result.startswith("Error:")


@pytest.mark.asyncio
async def test_calculate_invalid_expression_format():
    from . import calculate_handler
    result = await calculate_handler("!calculate 3++4")
    assert result.startswith("Error:")


@pytest.mark.asyncio
async def test_calculate_missing_operand():
    from . import calculate_handler
    result = await calculate_handler("!calculate 3+")
    assert result.startswith("Error:")


@pytest.mark.asyncio
async def test_calculate_only_operator():
    from . import calculate_handler
    result = await calculate_handler("!calculate +")
    assert result.startswith("Error:")


@pytest.mark.asyncio
async def test_calculate_multiple_operations():
    from . import calculate_handler
    result = await calculate_handler("!calculate 1+2+3+4")
    assert result == "1+2+3+4 = 10.0"


@pytest.mark.asyncio
async def test_calculate_subtraction_chain():
    from . import calculate_handler
    result = await calculate_handler("!calculate 10-2-3")
    assert result == "10-2-3 = 5.0"


@pytest.mark.asyncio
async def test_calculate_mixed_operations():
    from . import calculate_handler
    result = await calculate_handler("!calculate 5+3*2-4/2")
    assert result == "5+3*2-4/2 = 9.0"


@pytest.mark.asyncio
async def test_calculate_decimal_division():
    from . import calculate_handler
    result = await calculate_handler("!calculate 7/2")
    assert result == "7/2 = 3.5"


@pytest.mark.asyncio
async def test_calculate_zero_result():
    from . import calculate_handler
    result = await calculate_handler("!calculate 0*100")
    assert result == "0*100 = 0.0"


@pytest.mark.asyncio
async def test_calculate_negative_result():
    from . import calculate_handler
    result = await calculate_handler("!calculate 3-10")
    assert result == "3-10 = -7.0"


@pytest.mark.asyncio
async def test_calculate_invalid_pattern():
    from . import calculate_handler
    result = await calculate_handler("calculate 3+4")
    assert result == "Usage: !calculate <expression>\nExample: !calculate 3+4"


@pytest.mark.asyncio
async def test_calculate_large_numbers():
    from . import calculate_handler
    result = await calculate_handler("!calculate 1000000+2000000")
    assert result == "1000000+2000000 = 3000000.0"