"""Ping command - responds with pong."""
from __future__ import annotations
from typing import Optional
from . import command


@command(
    name="ping",
    description="Responds with 'pong'",
    pattern=r"^!ping$"
)
async def ping_handler(body: str) -> Optional[str]:
    """Simple ping command."""
    return "pong"
