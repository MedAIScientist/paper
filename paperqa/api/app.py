from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import shutil
from pathlib import Path
import asyncio

from paperqa import Docs, Settings, ask

# Set OpenAI key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable must be set")

app = FastAPI(title="PaperQA API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize global state
papers_dir = Path("papers")
papers_dir.mkdir(exist_ok=True)
docs = Docs()

class Query(BaseModel):
    question: str
    settings: Optional[Dict[str, Any]] = None

class UploadResponse(BaseModel):
    filename: str
    status: str
    message: str

@app.post("/upload")
async def upload_paper(file: UploadFile = File(...)):
    """Upload and index a PDF paper."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Save the file
        file_path = papers_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Add to docs
        await docs.aadd(str(file_path))
        
        return UploadResponse(
            filename=file.filename,
            status="success",
            message="File uploaded and indexed successfully"
        )
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_papers(query: Query):
    """Query the indexed papers."""
    try:
        settings = Settings(**(query.settings or {}))
        # Disable metadata fetching
        settings.disable_metadata = True
        
        # Initialize docs if not already initialized
        if not hasattr(docs, '_docs') or not docs._docs:
            await docs.aadd(str(papers_dir / "3765_ResiDual_Transformer_Alig.pdf"))
        
        response = await docs.aquery(
            query.question,
            settings=settings
        )
        
        return {
            "answer": str(response),
            "sources": []  # We'll add source handling later if needed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/papers")
async def list_papers():
    """List all uploaded papers."""
    try:
        papers = [f.name for f in papers_dir.glob("*.pdf")]
        return {"papers": papers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/papers/{filename}")
async def delete_paper(filename: str):
    """Delete a paper by filename."""
    try:
        file_path = papers_dir / filename
        if file_path.exists():
            file_path.unlink()
            return {"status": "success", "message": f"File {filename} deleted"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 