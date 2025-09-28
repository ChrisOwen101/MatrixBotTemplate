import asyncio
import pytest
from bot.handlers import generate_reply


@pytest.mark.asyncio
async def test_ping():
    assert await generate_reply("!ping") == "pong"


@pytest.mark.asyncio
async def test_greeting():
    resp = await generate_reply("Hello")
    assert "hello" in resp.lower()


@pytest.mark.asyncio
async def test_echo():
    msg = "This is a test"
    resp = await generate_reply(msg)
    assert resp == None
