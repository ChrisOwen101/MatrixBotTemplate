from __future__ import annotations
from typing import Optional
from . import command
import random

@command(
    name="tldr",
    description="generate an uncomfortably-honest 8-word summary of the current thread",
    pattern=r"^!tldr\s*(.*)$"
)
async def tldr_handler(body: str) -> Optional[str]:
    """Generate an uncomfortably-honest 8-word summary of the current thread.
    
    This command creates a brutally honest, satirical 8-word summary.
    Note: This is a mock implementation as actual thread analysis would require
    access to message history which isn't available in this handler signature.
    """
    
    summaries = [
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
    
    return random.choice(summaries)