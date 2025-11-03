"""Tests for command registry system."""
import pytest
from bot.commands import CommandRegistry, command


@pytest.mark.asyncio
async def test_registry_registration():
    """Test basic command registration."""
    registry = CommandRegistry()

    @command(name="test", description="Test command", pattern=r"^test$")
    async def test_handler(body: str):
        return "test response"

    # Note: decorator automatically registers with global registry
    # For isolated testing, we'd need to clear registry first
    assert registry.get_command("test") is not None


@pytest.mark.asyncio
async def test_registry_execute_matching():
    """Test executing a matching command."""
    from bot.commands import execute_command, get_registry

    # Commands should already be loaded from bot/commands/
    result = await execute_command("!ping")
    assert result == "pong"


@pytest.mark.asyncio
async def test_registry_execute_no_match():
    """Test executing with no matching command."""
    from bot.commands import execute_command

    result = await execute_command("this does not match any command")
    assert result is None


@pytest.mark.asyncio
async def test_list_commands():
    """Test listing all commands."""
    from bot.commands import get_registry

    registry = get_registry()
    commands = registry.list_commands()

    # Should have at least our basic commands
    assert len(commands) > 0
    command_names = [name for name, _ in commands]
    assert "ping" in command_names
