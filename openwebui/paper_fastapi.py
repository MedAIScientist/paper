from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:8888"] whichever is convenient
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(request: AskRequest):
    result = subprocess.run(
        ["pqa", "ask", request.query],
        cwd=".",  # or your custom path
        capture_output=True,
        text=True
    )
    return {"answer": result.stdout}

#uvicorn paper_fastapi:app --host 0.0.0.0 --port 8888 --reload