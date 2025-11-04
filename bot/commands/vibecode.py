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
    Generate the smallest runnable code snippet that accomplishes the user's described behavior.
    
    Args:
        body: The full message text containing the command and description
        
    Returns:
        A minimal, runnable code snippet or an error message
    """
    import re
    
    match = re.match(r"^!vibecode\s*(.*)$", body, re.DOTALL)
    if not match:
        return None
    
    description = match.group(1).strip()
    
    if not description:
        return "Please provide a description of what you want the code to do. Usage: !vibecode <description>"
    
    # Generate minimal code snippets based on common patterns
    desc_lower = description.lower()
    
    # HTTP request
    if any(word in desc_lower for word in ["http", "api", "request", "get", "post", "fetch", "curl"]):
        if "post" in desc_lower:
            return "```python\nimport requests\nresponse = requests.post('URL', json={'key': 'value'})\nprint(response.json())\n```"
        return "```python\nimport requests\nresponse = requests.get('URL')\nprint(response.json())\n```"
    
    # File operations
    if any(word in desc_lower for word in ["read file", "open file", "read from file"]):
        return "```python\nwith open('file.txt', 'r') as f:\n    data = f.read()\nprint(data)\n```"
    
    if any(word in desc_lower for word in ["write file", "save to file", "write to file"]):
        return "```python\nwith open('file.txt', 'w') as f:\n    f.write('content')\n```"
    
    # JSON operations
    if "parse json" in desc_lower or "load json" in desc_lower:
        return "```python\nimport json\ndata = json.loads('{\"key\": \"value\"}')\nprint(data['key'])\n```"
    
    if "json" in desc_lower and "file" in desc_lower:
        return "```python\nimport json\nwith open('data.json') as f:\n    data = json.load(f)\nprint(data)\n```"
    
    # List operations
    if "sort" in desc_lower and "list" in desc_lower:
        return "```python\nitems = [3, 1, 2]\nitems.sort()\nprint(items)\n```"
    
    if "reverse" in desc_lower and "list" in desc_lower:
        return "```python\nitems = [1, 2, 3]\nitems.reverse()\nprint(items)\n```"
    
    # String operations
    if "split string" in desc_lower:
        return "```python\ntext = 'hello world'\nwords = text.split()\nprint(words)\n```"
    
    if "join" in desc_lower and ("list" in desc_lower or "array" in desc_lower):
        return "```python\nitems = ['a', 'b', 'c']\nresult = ','.join(items)\nprint(result)\n```"
    
    # Date/time
    if any(word in desc_lower for word in ["current time", "now", "timestamp", "current date"]):
        return "```python\nfrom datetime import datetime\nprint(datetime.now())\n```"
    
    # Web scraping
    if any(word in desc_lower for word in ["scrape", "parse html", "beautifulsoup"]):
        return "```python\nfrom bs4 import BeautifulSoup\nimport requests\nhtml = requests.get('URL').text\nsoup = BeautifulSoup(html, 'html.parser')\nprint(soup.find('tag'))\n```"
    
    # Database
    if "sqlite" in desc_lower or ("database" in desc_lower and "query" in desc_lower):
        return "```python\nimport sqlite3\ncon = sqlite3.connect('db.sqlite')\ncur = con.cursor()\nresult = cur.execute('SELECT * FROM table').fetchall()\nprint(result)\n```"
    
    # Random
    if "random" in desc_lower:
        if "choice" in desc_lower or "pick" in desc_lower:
            return "```python\nimport random\nitems = [1, 2, 3]\nprint(random.choice(items))\n```"
        return "```python\nimport random\nprint(random.randint(1, 100))\n```"
    
    # Sleep/wait
    if "sleep" in desc_lower or "wait" in desc_lower:
        return "```python\nimport time\ntime.sleep(1)  # seconds\n```"
    
    # Environment variable
    if "environment variable" in desc_lower or "env var" in desc_lower:
        return "```python\nimport os\nvalue = os.getenv('VAR_NAME', 'default')\nprint(value)\n```"
    
    # Command line arguments
    if "command line" in desc_lower or "argv" in desc_lower or "arguments" in desc_lower:
        return "```python\nimport sys\nargs = sys.argv[1:]  # exclude script name\nprint(args)\n```"
    
    # CSV
    if "csv" in desc_lower:
        if "write" in desc_lower:
            return "```python\nimport csv\nwith open('data.csv', 'w', newline='') as f:\n    writer = csv.writer(f)\n    writer.writerow(['col1', 'col2'])\n```"
        return "```python\nimport csv\nwith open('data.csv') as f:\n    reader = csv.reader(f)\n    for row in reader:\n        print(row)\n```"
    
    # Default response
    return f"I'll create a minimal snippet for: {description}\n\n```python\n# {description}\npass  # Replace with your implementation\n```\n\nNote: Please be more specific about the task (e.g., 'read a file', 'make HTTP request', 'parse JSON') for a better snippet."