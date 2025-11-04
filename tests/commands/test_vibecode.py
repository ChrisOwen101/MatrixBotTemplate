import pytest
from typing import Optional


@pytest.mark.asyncio
async def test_vibecode_hello_world():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode print hello world")
    assert result is not None
    assert "Hello, World!" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_read_file():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode read a file")
    assert result is not None
    assert "open" in result
    assert "read()" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_write_file():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode write to a file")
    assert result is not None
    assert "open" in result
    assert '"w"' in result
    assert "write" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_http_request():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode make an http request")
    assert result is not None
    assert "requests" in result
    assert "get" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_sort_list():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode sort a list")
    assert result is not None
    assert "sort()" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_reverse_list():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode reverse a list")
    assert result is not None
    assert "reverse()" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_reverse_string():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode reverse a string")
    assert result is not None
    assert "[::-1]" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_loop():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode create a loop")
    assert result is not None
    assert "for" in result
    assert "range" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_function():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode define a function")
    assert result is not None
    assert "def" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_class():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode create a class")
    assert result is not None
    assert "class" in result
    assert "__init__" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_dictionary():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode work with a dictionary")
    assert result is not None
    assert "```python" in result
    assert "{" in result and "}" in result


@pytest.mark.asyncio
async def test_vibecode_json_parse():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode parse json")
    assert result is not None
    assert "json" in result
    assert "loads" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_json_dump():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode write json")
    assert result is not None
    assert "json" in result
    assert "dumps" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_current_time():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode get current time")
    assert result is not None
    assert "datetime" in result
    assert "now()" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_random_number():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode generate a random number")
    assert result is not None
    assert "random" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_web_scraping():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode scrape a website")
    assert result is not None
    assert "BeautifulSoup" in result
    assert "requests" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_empty_description():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode")
    assert result is not None
    assert "Please provide a description" in result
    assert "Usage:" in result


@pytest.mark.asyncio
async def test_vibecode_whitespace_only():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode   ")
    assert result is not None
    assert "Please provide a description" in result


@pytest.mark.asyncio
async def test_vibecode_unknown_request():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode do something very obscure and unrecognized")
    assert result is not None
    assert "need more specific details" in result
    assert "Try describing" in result


@pytest.mark.asyncio
async def test_vibecode_case_insensitive():
    from . import vibecode_handler
    result = await vibecode_handler("!VIBECODE hello world")
    assert result is not None
    assert "Hello, World!" in result


@pytest.mark.asyncio
async def test_vibecode_multiline_description():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode create a function\nthat does something")
    assert result is not None
    assert "def" in result


@pytest.mark.asyncio
async def test_vibecode_api_request():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode fetch data from an api")
    assert result is not None
    assert "requests" in result
    assert "get" in result


@pytest.mark.asyncio
async def test_vibecode_iterate():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode iterate over items")
    assert result is not None
    assert "for" in result
    assert "```python" in result


@pytest.mark.asyncio
async def test_vibecode_invalid_pattern():
    from . import vibecode_handler
    result = await vibecode_handler("not a vibecode command")
    assert result is None


@pytest.mark.asyncio
async def test_vibecode_get_url():
    from . import vibecode_handler
    result = await vibecode_handler("!vibecode get url content")
    assert result is not None
    assert "requests" in result
    assert "get" in result