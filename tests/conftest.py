"""Pytest configuration and fixtures."""
import pytest


@pytest.fixture
def sample_message():
    """Sample message body for testing."""
    return "test message"


@pytest.fixture
def bot_config():
    """Mock bot configuration."""
    from bot.config import BotConfig

    return BotConfig(
        homeserver="https://matrix.example.com",
        user_id="@testbot:example.com",
        device_id="TEST_DEVICE",
        display_name="Test Bot",
        log_level="INFO",
        allowed_rooms=["!test:example.com"],
        enable_auto_commit=False
    )
