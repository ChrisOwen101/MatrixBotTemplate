# Matrix Echo Bot

A simple Matrix bot written in Python using [`matrix-nio`](https://github.com/poljar/matrix-nio). It logs in with an access token, listens for text messages, and replies.

## Features

- Async Matrix client with `matrix-nio`
- Simple reply logic (ping, greetings, echo fallback)
- Config via `config.toml` + `.env` for secret token
- Graceful shutdown on SIGINT/SIGTERM
- Basic tests for reply logic

## Quick Start

1. Create & activate a virtual environment (Python 3.11+ recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example config and edit it:

```bash
cp config.example.toml config.toml
$EDITOR config.toml
```

4. Create a `.env` file containing your access token:

```bash
echo 'MATRIX_ACCESS_TOKEN="syt_xxx"' > .env
```

(You can obtain an access token by logging in with another client or by using the Matrix login API.)

5. Run the bot:

```bash
python -m bot.main
```

## Extending Reply Logic

Edit `bot/handlers.py` and expand `generate_reply` to parse commands or integrate AI/NLP. Ensure you keep responses below ~4000 chars.

## Testing

```bash
pytest -q
```

## Production Suggestions

- Persist sync token using a store (e.g., `SqliteStore`) to avoid missed events
- Add retry/backoff for network issues
- Add structured logging / metrics
- Use application service or bot user with limited permissions

## License

MIT (add a LICENSE file if you plan to distribute)
