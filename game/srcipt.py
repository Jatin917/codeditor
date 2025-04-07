import requests
import os

# Path to your project folder with 6 .py files
project_dir = "./"

# List your files here (including main.py)
file_names = [
    "bot.py",
    "deck.py",
    "rules.py",
    "utils.py",
    "game.py",
    "main.py"
]

files_payload = []

# Read and prepare file contents
for fname in file_names:
    with open(os.path.join(project_dir, fname), "r") as f:
        content = f.read()
        files_payload.append({
            "name": fname,
            "content": content
        })

# Build payload
payload = {
    "language": "python3",
    "version": "3.10.0",
    "files": files_payload
}

# Send request to Piston
url = "https://emkc.org/api/v2/piston/execute"
response = requests.post(url, json=payload)

# Print output
result = response.json()
print("OUTPUT:")
print(result.get("run", {}).get("stdout", "No output"))
print("ERRORS:")
print(result.get("run", {}).get("stderr", "No errors"))
