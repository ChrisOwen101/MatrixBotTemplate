from __future__ import annotations
from typing import Optional
from . import command

@command(
    name="vibecode",
    description="reply with the smallest runnable snippet that accomplishes the user's described behavior",
    pattern=r"^!vibecode\s*(.*)$"
)
async def vibecode_handler(body: str) -> Optional[str]:
    """
    Generate the smallest runnable code snippet for a described behavior.
    
    Usage: !vibecode <description of what the code should do>
    
    Returns a minimal, executable code snippet that accomplishes the requested task.
    """
    import re
    
    match = re.match(r"^!vibecode\s*(.*)$", body.strip(), re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    
    description = match.group(1).strip()
    
    if not description:
        return "Please provide a description of what you want the code to do.\n\nUsage: !vibecode <description>"
    
    # Generate minimal code snippets based on common requests
    description_lower = description.lower()
    
    # Hello world variants
    if "hello" in description_lower and "world" in description_lower:
        return '```python\nprint("Hello, World!")\n```'
    
    # File operations
    if "read" in description_lower and "file" in description_lower:
        return '```python\nwith open("file.txt") as f:\n    content = f.read()\n```'
    
    if "write" in description_lower and "file" in description_lower:
        return '```python\nwith open("file.txt", "w") as f:\n    f.write("content")\n```'
    
    # HTTP requests
    if any(word in description_lower for word in ["http", "request", "api", "fetch", "get url"]):
        return '```python\nimport requests\nr = requests.get("https://example.com")\nprint(r.text)\n```'
    
    # List/array operations
    if "sort" in description_lower and ("list" in description_lower or "array" in description_lower):
        return '```python\nlst = [3, 1, 4, 1, 5]\nlst.sort()\nprint(lst)\n```'
    
    if "reverse" in description_lower and ("list" in description_lower or "array" in description_lower):
        return '```python\nlst = [1, 2, 3, 4, 5]\nlst.reverse()\nprint(lst)\n```'
    
    # String operations
    if "reverse" in description_lower and "string" in description_lower:
        return '```python\ns = "hello"\nprint(s[::-1])\n```'
    
    # Loop examples
    if "loop" in description_lower or "iterate" in description_lower:
        return '```python\nfor i in range(10):\n    print(i)\n```'
    
    # Function definition
    if "function" in description_lower or "def" in description_lower:
        return '```python\ndef func(x):\n    return x * 2\n```'
    
    # Class definition
    if "class" in description_lower:
        return '```python\nclass MyClass:\n    def __init__(self, value):\n        self.value = value\n```'
    
    # Dictionary operations
    if "dictionary" in description_lower or "dict" in description_lower:
        return '```python\nd = {"key": "value"}\nprint(d["key"])\n```'
    
    # JSON operations
    if "json" in description_lower and "parse" in description_lower:
        return '```python\nimport json\ndata = json.loads(\'{"key": "value"}\')\n```'
    
    if "json" in description_lower and ("write" in description_lower or "dump" in description_lower):
        return '```python\nimport json\ndata = {"key": "value"}\nprint(json.dumps(data))\n```'
    
    # Date/time
    if "current" in description_lower and ("time" in description_lower or "date" in description_lower):
        return '```python\nfrom datetime import datetime\nprint(datetime.now())\n```'
    
    # Random number
    if "random" in description_lower:
        return '```python\nimport random\nprint(random.randint(1, 100))\n```'
    
    # Web scraping
    if "scrape" in description_lower or "parse html" in description_lower:
        return '```python\nfrom bs4 import BeautifulSoup\nimport requests\nhtml = requests.get("https://example.com").text\nsoup = BeautifulSoup(html, "html.parser")\n```'
    
    # Default response
    return f"I need more specific details to generate a code snippet for: '{description}'\n\nTry describing a specific programming task like:\n- read a file\n- make an HTTP request\n- sort a list\n- reverse a string"