import re
import subprocess

def handle_user_code(user_code: str):
    # Inject user code into player.py
    try:
        with open("player.py", "r") as f:
            content = f.read()

        new_code = f"# ---USER-CODE-START---\n{user_code}\n# ---USER-CODE-END---"

        updated_content = re.sub(
            r"# ---USER-CODE-START---(.*?)# ---USER-CODE-END---",
            new_code,
            content,
            flags=re.DOTALL
        )

        with open("player.py", "w") as f:
            f.write(updated_content)
    except Exception as e:
        return {"success": False, "error": f"Injection failed: {str(e)}"}

    # Execute the game logic in main.py
    try:
        result = subprocess.run(
            ["python3", "main.py"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return {
            "success": True,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Code execution timed out!"}

    except Exception as e:
        return {"success": False, "error": str(e)}
