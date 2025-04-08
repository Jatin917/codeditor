from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

@app.route('/submit', methods=['POST'])
def submit():
    user_code = request.json.get("code")

    # Save the submitted code to playerSubmitted.py
    with open("playerSubmitted.py", "w") as f:
        f.write(user_code)

    try:
        # Run the main.py that uses playerSubmitted.py
        result = subprocess.run(
            ["python", "main.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out"}), 408


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
