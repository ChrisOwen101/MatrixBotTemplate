## AI Assistant Working Guide (Concise)

Purpose: Lightweight Matrix echo-style bot using `matrix-nio`; prioritize clarity, small surface area, and testable pure logic.

Key Files:

- `bot/config.py` load + validate `config.toml`, exposes `BotConfig.access_token` from env (`MATRIX_ACCESS_TOKEN` via `.env`). Fail fast if missing.
- `bot/handlers.py` `generate_reply` (pure: returns string or None) and `on_message` (filters + sends). Timestamp filter: ignore events with `server_timestamp < START_TIME_MS - HISTORICAL_SKEW_MS` (5s skew). Hard‑coded room substring filter currently (`BHXRvKRXKeMuirqrlY`).
- `bot/main.py` bootstrap: load config, create `AsyncClient`, wrap event callback, inject access token (no password login), sync loop with simple retry (5s sleep on exception), graceful shutdown via signals.
- `tests/` cover command replies and timestamp filtering; use dummy client/room/event objects.

Core Conventions:

1. Keep reply generation pure (no network / I/O) and short (< ~4000 chars). Return None to skip sending.
2. Add new commands by extending `generate_reply`; refactor to a registry only when it grows (see comment in original long instructions).
3. Do not print or log the access token. Secrets only via environment.
4. Maintain backward compatibility with tests when altering filtering or room logic; add/adjust tests if behavior changes.
5. Logging: structured via stdlib; prefer `logger.exception` inside broad catch blocks at handler boundaries only.

Typical Dev Workflow:

1. Create venv + install deps: `pip install -r requirements.txt`.
2. Copy `config.example.toml` → `config.toml`; create `.env` with `MATRIX_ACCESS_TOKEN`.
3. Run bot: `python -m bot.main`.
4. Run tests: `pytest -q` (async tests use `pytest-asyncio`).

Extension Points (low-risk):

- Add command: modify `generate_reply`; add a unit test in `tests/test_handlers.py` (happy path + one edge case / None case).
- Room allow‑list: replace substring filter with config key (`allowed_rooms: list[str]`); update tests (one allowed, one skipped).
- Retry/backoff improvements: wrap `client.sync` with incremental sleep (ensure cancellation respects `STOP`).

Testing Patterns:

- Use lightweight dummy classes (see `test_timestamp_filter.py`) rather than heavy mocking frameworks.
- Keep START_TIME_MS logic intact; if changing skew constant update tests accordingly.

Gotchas / Avoid:

- Access token not set → `BotConfig.access_token` raises RuntimeError (tests assume env present if accessed). Handle before network calls.
- Attribute confusion: `client.user_id` must be set manually when injecting existing token (handled in `login_if_needed`).
- Hard-coded room filter currently limits replies; altering it without tests may cause spam in unintended rooms.

When Opening a PR:

- Single focused change, update README if user-facing. Add/adjust tests for new behavior. Keep dependency additions minimal and justified.

If Unsure: open a small PR or ask for clarification instead of large refactors.

Last updated: 2025-09-28 (concise rewrite)
