import pytest
import re
from typing import Optional

# Import the tldr handler from bot.commands.tldr
from bot.commands.tldr import tldr_handler


@pytest.mark.asyncio
async def test_tldr_returns_string():
    """Test that tldr returns a string response."""
    result = await tldr_handler("!tldr")
    assert result is not None
    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_tldr_returns_8_words():
    """Test that the returned summary contains exactly 8 words."""
    result = await tldr_handler("!tldr")
    assert result is not None
    word_count = len(result.split())
    assert word_count == 8, f"Expected 8 words, got {word_count}: {result}"


@pytest.mark.asyncio
async def test_tldr_with_empty_input():
    """Test tldr with empty string input."""
    result = await tldr_handler("")
    assert result is not None
    assert isinstance(result, str)
    assert len(result.split()) == 8


@pytest.mark.asyncio
async def test_tldr_with_additional_text():
    """Test tldr ignores additional text after command."""
    result = await tldr_handler("!tldr some extra text here")
    assert result is not None
    assert isinstance(result, str)
    assert len(result.split()) == 8


@pytest.mark.asyncio
async def test_tldr_returns_from_predefined_list():
    """Test that tldr returns one of the predefined summaries."""
    expected_summaries = [
        "Everyone argues but nobody actually reads the links",
        "Strong opinions expressed with zero supporting evidence provided",
        "Derailed into arguing about something completely different now",
        "Same debate recycled for the hundredth time today",
        "Everyone agrees violently while using different words exactly",
        "Nobody knows what they're talking about here honestly",
        "Confidently incorrect people explaining things to actual experts",
        "Could have been resolved with simple Google search",
        "People talking past each other without realizing it",
        "Thread died when someone asked for actual sources",
        "Argument over semantics instead of the actual issue",
        "Everyone stopped reading after the first two messages",
        "Passive aggressive subtweets disguised as helpful advice responses",
        "Main point lost in increasingly pedantic side arguments",
        "Confidently stating opinions as if they were facts",
        "Circular argument that went nowhere but wasted time",
        "People agreeing with different interpretations of same thing",
        "Unnecessary drama over something that doesn't matter really",
        "Strong feelings about topic nobody will remember tomorrow",
        "Walls of text that nobody will actually read"
    ]
    
    result = await tldr_handler("!tldr")
    assert result in expected_summaries


@pytest.mark.asyncio
async def test_tldr_multiple_calls_can_return_different_results():
    """Test that tldr can return different summaries (randomness check)."""
    results = set()
    for _ in range(50):
        result = await tldr_handler("!tldr")
        results.add(result)
    
    # With 20 possible summaries and 50 calls, we should get multiple different ones
    assert len(results) > 1, "Expected some variety in responses"


@pytest.mark.asyncio
async def test_tldr_with_whitespace():
    """Test tldr with various whitespace patterns."""
    result = await tldr_handler("!tldr   ")
    assert result is not None
    assert isinstance(result, str)
    assert len(result.split()) == 8


@pytest.mark.asyncio
async def test_tldr_never_returns_none():
    """Test that tldr always returns a string, never None."""
    for _ in range(10):
        result = await tldr_handler("!tldr")
        assert result is not None


@pytest.mark.asyncio
async def test_tldr_never_returns_empty_string():
    """Test that tldr never returns an empty string."""
    for _ in range(10):
        result = await tldr_handler("!tldr")
        assert result != ""
        assert len(result) > 0