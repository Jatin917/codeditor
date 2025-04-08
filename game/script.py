import requests
import os

# Absolute path to project folder (same folder as script)
project_dir = os.path.dirname(os.path.abspath(__file__))

# Name of the combined file
file_names = ["combined_project.py"]

# Read file content and prepare payload
files_payload = []
for filename in file_names:
    file_path = os.path.join(project_dir, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        files_payload.append({
            "name": filename,
            "content": f.read()
        })

# Create the payload for piston
payload = {
    "language": "python",
    "version": "3.10.0",
    "files": files_payload
}

# Send the request
url = "https://emkc.org/api/v2/piston/execute"
response = requests.post(url, json=payload)

# Parse and show result
result = response.json()

print("----- OUTPUT -----")
print(result.get("run", {}).get("stdout", "No output"))

print("----- ERRORS -----")
print(result.get("run", {}).get("stderr", "No errors"))
