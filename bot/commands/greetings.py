"""Greeting commands - responds to hi, hello, hey."""
from __future__ import annotations
from typing import Optional
from . import command


@command(
    name="greetings",
    description="Responds to greetings (hi, hello, hey)",
    pattern=r"^(hi|hello|hey)$"
)
async def greeting_handler(body: str) -> Optional[str]:
    """Respond to simple greetings."""
    return "Hello! I'm The Architect, a self-modifying Matrix bot. Use !list to see available commands."
