import pytest
from typing import Optional


@pytest.mark.asyncio
async def test_vibecode_empty_command():
    """Test vibecode with just the command and no description."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode")
    assert result == "Please provide a description of what you want the code to do. Usage: !vibecode <description>"


@pytest.mark.asyncio
async def test_vibecode_whitespace_only():
    """Test vibecode with only whitespace after command."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode   ")
    assert result == "Please provide a description of what you want the code to do. Usage: !vibecode <description>"


@pytest.mark.asyncio
async def test_vibecode_invalid_pattern():
    """Test vibecode with text that doesn't match the pattern."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("vibecode make a request")
    assert result is None


@pytest.mark.asyncio
async def test_vibecode_http_get_request():
    """Test vibecode for HTTP GET request."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode make an http get request")
    assert result is not None
    assert "requests.get" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_http_post_request():
    """Test vibecode for HTTP POST request."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode make a post request to api")
    assert result is not None
    assert "requests.post" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_read_file():
    """Test vibecode for reading a file."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode read file")
    assert result is not None
    assert "open(" in result
    assert "'r'" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_write_file():
    """Test vibecode for writing to a file."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode write to file")
    assert result is not None
    assert "open(" in result
    assert "'w'" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_parse_json():
    """Test vibecode for parsing JSON."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode parse json string")
    assert result is not None
    assert "json.loads" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_json_file():
    """Test vibecode for loading JSON from file."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode read json file")
    assert result is not None
    assert "json.load" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_sort_list():
    """Test vibecode for sorting a list."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode sort a list")
    assert result is not None
    assert "sort()" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_reverse_list():
    """Test vibecode for reversing a list."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode reverse a list")
    assert result is not None
    assert "reverse()" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_split_string():
    """Test vibecode for splitting a string."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode split string")
    assert result is not None
    assert "split()" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_join_list():
    """Test vibecode for joining a list."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode join list items")
    assert result is not None
    assert "join(" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_current_time():
    """Test vibecode for getting current time."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode get current time")
    assert result is not None
    assert "datetime" in result
    assert "now()" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_web_scraping():
    """Test vibecode for web scraping."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode scrape a webpage")
    assert result is not None
    assert "BeautifulSoup" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_sqlite_query():
    """Test vibecode for SQLite database query."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode query sqlite database")
    assert result is not None
    assert "sqlite3" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_random_number():
    """Test vibecode for generating random number."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode generate random number")
    assert result is not None
    assert "random" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_random_choice():
    """Test vibecode for random choice from list."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode pick random choice from list")
    assert result is not None
    assert "random.choice" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_sleep():
    """Test vibecode for sleep/wait."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode sleep for 1 second")
    assert result is not None
    assert "time.sleep" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_environment_variable():
    """Test vibecode for getting environment variable."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode get environment variable")
    assert result is not None
    assert "os.getenv" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_command_line_args():
    """Test vibecode for command line arguments."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode parse command line arguments")
    assert result is not None
    assert "sys.argv" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_read_csv():
    """Test vibecode for reading CSV file."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode read csv file")
    assert result is not None
    assert "csv.reader" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_write_csv():
    """Test vibecode for writing CSV file."""
    from vibecode import vibecode_handler
    
    result = await vibecode_handler("!vibecode write csv file")
    assert result is not None
    assert "csv.writer" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_default_response():
    """Test vibecode with unrecognized description."""
    from vibecode import vibecode