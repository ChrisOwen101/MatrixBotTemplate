# The Architect - Self-Modifying Matrix Bot

A self-modifying Matrix bot written in Python using [`matrix-nio`](https://github.com/poljar/matrix-nio) and Claude AI. The Architect can dynamically generate and add new commands to itself using natural language descriptions.

## Features

- **Self-Modifying**: Add new commands using natural language via `/add` command
- **Claude AI Integration**: Uses Claude API to generate command code
- **Dynamic Command System**: Commands are loaded from individual Python modules
- **Code Validation**: Automatically validates generated code for safety and correctness
- **Git Integration**: Auto-commits all code changes with descriptive messages
- **Auto-Restart**: Bot automatically restarts to load new commands
- **Test Generation**: Automatically generates tests for new commands
- Async Matrix client with `matrix-nio`
- Config via `config.toml` + `.env` for secret tokens
- Graceful shutdown on SIGINT/SIGTERM
- Comprehensive test suite

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

4. Create a `.env` file containing your tokens:

```bash
echo 'MATRIX_ACCESS_TOKEN="syt_xxx"' > .env
echo 'ANTHROPIC_API_KEY="sk-ant-xxx"' >> .env
```

You'll need:
- **Matrix Access Token**: Obtain by logging in with another client or using the Matrix login API
- **Anthropic API Key**: Get from https://console.anthropic.com/

5. Run the bot:

```bash
python -m bot.main
```

## Using The Architect

### Built-in Commands

- `!ping` - Responds with "pong"
- `hi`, `hello`, `hey` - Greeting response
- `/list` - List all available commands
- `/add -n <name> -d "<description>"` - Add a new command using AI
- `/remove <name>` - Remove a dynamically added command

### Adding New Commands

Use the `/add` command to create new functionality:

```
/add -n calculate -d "Calculate mathematical expressions like 2+2 or 10*5"
```

The bot will:
1. Use Claude AI to generate the command code
2. Validate the generated code for safety
3. Generate tests for the command
4. Save the code to `bot/commands/<name>.py`
5. Commit the changes to git (if enabled)
6. Restart to load the new command

After the restart, you can use your new command:
```
/calculate 2+2
```

### Removing Commands

```
/remove calculate
```

This will remove the command file, tests, commit the removal, and restart the bot.

## Architecture

### Directory Structure

```
bot/
  commands/          # Dynamic command modules
    __init__.py      # Command registry and loader
    ping.py          # Built-in commands
    greetings.py
    list.py          # Meta-commands
    add.py
    remove.py
    <custom>.py      # Your dynamically added commands
  config.py          # Configuration management
  handlers.py        # Message event handlers
  main.py            # Bot lifecycle and Matrix client
  claude_integration.py  # Claude API client
  code_validator.py  # Code safety validation
  git_integration.py # Git operations
  reload.py          # Bot restart mechanism

tests/
  commands/          # Tests for commands
  conftest.py        # Test fixtures
  test_*.py          # Test modules
```

### Command Registry System

Commands are automatically discovered and loaded from `bot/commands/` directory. Each command is a Python module with:

```python
from bot.commands import command
from typing import Optional

@command(
    name="mycommand",
    description="What this command does",
    pattern=r"^/mycommand\s*(.*)$"
)
async def mycommand_handler(body: str) -> Optional[str]:
    """Handler implementation."""
    return "Response"
```

The `@command` decorator registers the command with the registry. The pattern is a regex that matches the command invocation.

### Code Generation Flow

1. User sends `/add -n <name> -d "<description>"`
2. `add.py` command handler parses arguments
3. Claude API generates command code based on description
4. Code validator checks for:
   - Syntax errors
   - Required function structure
   - Dangerous operations (file access, subprocess, etc.)
5. Code is written to `bot/commands/<name>.py`
6. Tests are generated and written to `tests/commands/test_<name>.py`
7. Changes are committed to git (if `enable_auto_commit` is true)
8. Bot restarts using `os.execv()` to load new code

### Safety Features

- **AST Validation**: Generated code is parsed and validated before execution
- **Dangerous Operation Detection**: Blocks imports like `subprocess`, `os.system`, `eval`, `exec`
- **Compilation Check**: Code must compile before being saved
- **Test Generation**: Each command gets tests to verify functionality
- **Git Tracking**: All changes are version controlled
- **Protected Commands**: Core commands (`add`, `remove`, `list`) cannot be removed

## Testing

```bash
# Run all tests
pytest -q

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_command_registry.py -v
```

## Configuration

Edit `config.toml`:

```toml
[bot]
homeserver = "https://matrix.example.com"
user_id = "@bot:example.com"
device_id = "DEV1"
display_name = "The Architect"
log_level = "DEBUG"

# List of allowed room IDs
allowed_rooms = ["!roomid:example.com"]

# Enable automatic git commits for code changes
enable_auto_commit = true
```

## Production Suggestions

- Review all generated code before committing to production
- Set up a separate development bot for testing new commands
- Use branch protection on main branch
- Monitor Claude API usage and costs
- Implement command permission system (currently anyone in allowed rooms can add commands)
- Add command usage logging/analytics
- Persist sync token using `SqliteStore` for production reliability
- Set up monitoring/alerting for bot restarts

## License

MIT (add a LICENSE file if you plan to distribute)
