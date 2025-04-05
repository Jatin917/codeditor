from fastapi import FastAPI
from pydantic import BaseModel
import run  # Import your controller logic

app = FastAPI()

class CodeInput(BaseModel):
    userCode: str

@app.post("/submit")
async def submit_code(code: CodeInput):
    result = run.handle_user_code(code.userCode)
    return result
