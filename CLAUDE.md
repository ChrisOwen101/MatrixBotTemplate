# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lightweight Matrix echo-style bot using `matrix-nio`. The bot logs in with an access token, listens for text messages in allowed rooms, and replies based on simple command logic. Architecture prioritizes clarity, small surface area, and testable pure logic.

## Development Commands

### Setup
```bash
# Create and activate virtual environment (Python 3.11+ required)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy example config and edit
cp config.example.toml config.toml
# Create .env file with: MATRIX_ACCESS_TOKEN="syt_xxx"
```

### Running
```bash
# Run the bot
python -m bot.main
```

### Testing
```bash
# Run all tests
pytest -q

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_handlers.py -v
```

## Architecture

### Core Components

**bot/config.py** - Configuration management
- Loads and validates `config.toml` using `tomllib` (Python 3.11+) or `tomli` fallback
- Exposes `BotConfig.access_token` from environment via `MATRIX_ACCESS_TOKEN` (loaded from `.env`)
- Fails fast if required config keys are missing
- Config keys: `homeserver`, `user_id`, `device_id`, `display_name`, `log_level`

**bot/handlers.py** - Message handling and reply logic
- `generate_reply(body: str) -> str | None`: Pure function containing all reply logic. Returns None to skip sending a reply.
- `on_message(client, room, event)`: Event handler that filters messages and sends replies
- Timestamp filtering: Ignores historical events with `server_timestamp < START_TIME_MS - HISTORICAL_SKEW_MS` (5s skew allowance) to avoid replying to old messages on first sync
- Room filtering: Hard-coded `ALLOWED_ROOMS` list currently checks if `room.room_id` is in the list

**bot/main.py** - Bot lifecycle and Matrix client
- Bootstraps bot: loads config, creates `AsyncClient`, registers event callbacks
- `login_if_needed()`: Injects pre-issued access token (no password login). Manually sets `client.user_id` since nio doesn't populate it when using token injection.
- Sync loop with basic retry (5s sleep on exception)
- Signal handlers for graceful shutdown on SIGINT/SIGTERM (sets `STOP` event)

### Key Architectural Decisions

1. **Pure reply logic**: `generate_reply` is pure (no I/O) to keep it testable. Keep responses under ~4000 chars.

2. **Token injection pattern**: Uses pre-issued access token rather than password login. The `client.user_id` must be set manually when injecting tokens (handled in `login_if_needed` at bot/main.py:42).

3. **Historical event filtering**: Uses bot start time (`START_TIME_MS`) to filter old messages during initial sync, preventing replies to historical messages.

4. **Room allowlist**: Currently uses hard-coded room ID list in `ALLOWED_ROOMS` (bot/handlers.py:13). When extending, consider moving to config.

## Development Patterns

### Adding New Commands
Extend `generate_reply` in `bot/handlers.py`. Keep logic pure and return None when no reply is needed:
```python
async def generate_reply(body: str) -> str | None:
    body_lower = body.strip().lower()
    if body_lower.startswith("!mycommand"):
        return "My response"
    # ... existing logic
```
Add corresponding tests in `tests/test_handlers.py`.

### Testing Patterns
- Use lightweight dummy classes rather than heavy mocking frameworks (see existing tests)
- Test both happy paths and edge cases (especially None returns)
- When changing timestamp or room filtering logic, update corresponding tests

### Security
- Never log or print the access token
- All secrets must be loaded from environment variables (via `.env` file)
- Access token not set → `BotConfig.access_token` raises `RuntimeError` before any network calls

### Extension Points
- **New commands**: Modify `generate_reply`; consider command registry pattern only when it grows significantly
- **Room allowlist**: Move `ALLOWED_ROOMS` to config.toml as `allowed_rooms: list[str]`
- **Retry/backoff**: Wrap `client.sync` with exponential backoff (ensure cancellation respects `STOP` event)
- **Persistence**: Add `SqliteStore` to persist sync tokens and avoid processing missed events

## Important Gotchas

1. **Manual user_id assignment**: When injecting access token, must manually set `client.user_id` (see bot/main.py:42). The nio library doesn't populate this automatically.

2. **Hard-coded room filter**: Current `ALLOWED_ROOMS` filter prevents spam but limits functionality. Changing without updating tests may cause unintended behavior.

3. **Timestamp filtering**: The `START_TIME_MS` and `HISTORICAL_SKEW_MS` constants prevent historical replies. Modifying these affects first-sync behavior.

4. **Backward compatibility**: Maintain test compatibility when altering filtering or room logic.
