import requests
import time

# Replace with your RapidAPI key
api_key = "YOUR_RAPIDAPI_KEY"

# Endpoint & headers
url = "https://judge0-ce.p.rapidapi.com/submissions"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
    "content-type": "application/json"
}

# Your Python code
code = """
print("Hello from Judge0!")
for i in range(3):
    print("Judge0 count:", i)
"""

# Payload
payload = {
    "language_id": 71,  # Python 3
    "source_code": code,
    "stdin": "",        # Add input if needed
}

# Submit code
response = requests.post(url, json=payload, headers=headers)
token = response.json()["token"]

# Wait for execution
time.sleep(2)

# Fetch result
result_response = requests.get(f"{url}/{token}", headers=headers)
result = result_response.json()

print("----- OUTPUT -----")
print(result.get("stdout", "No output"))

print("----- ERRORS -----")
print(result.get("stderr", "No errors"))
