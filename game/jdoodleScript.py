import requests

# Replace with your JDoodle API credentials
client_id = "your_client_id"
client_secret = "your_client_secret"

# Read code from a file (e.g., hello.py)
with open("combined_project.py", "r") as file:
    code = file.read()

# Payload for the API request
data = {
    "clientId": '929e348cd89be4f1b95ea655eb4b851d',
    "clientSecret": '4baf74c8622f45be1ac368af42d35e3b15c83bde40ee5bb1bcdfa86d0173eccc',
    "script": code,
    "language": "python3",
    "versionIndex": "3",
}

# Send POST request
response = requests.post("https://api.jdoodle.com/v1/execute", json=data)

# Print the response
if response.status_code == 200:
    result = response.json()
    print("Output:", result.get("output"))
else:
    print("Error:", response.status_code, response.text)
