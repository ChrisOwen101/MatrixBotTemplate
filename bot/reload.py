"""Bot reload mechanism for applying code changes."""
from __future__ import annotations
import os
import sys
import logging

logger = logging.getLogger(__name__)


def restart_bot() -> None:
    """
    Restart the bot process.

    This uses os.execv() to replace the current process with a new one,
    maintaining the same process ID and ensuring a clean restart.
    """
    logger.info("Restarting bot...")

    try:
        # Get the Python executable and original arguments
        python = sys.executable
        args = [python] + sys.argv

        # Close file descriptors to avoid issues
        # (nio client should be closed before this is called)

        # Replace the current process with a new one
        os.execv(python, args)

    except Exception as e:
        logger.exception(f"Failed to restart bot: {e}")
        # If restart fails, we should at least try to continue running
        raise RuntimeError(f"Bot restart failed: {e}")
