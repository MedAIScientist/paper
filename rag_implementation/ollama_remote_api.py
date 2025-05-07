#This is GPU server connection via TUBITAK GPU2 required, you cannot run it locally
#Also do not forget to configure OLLAMA BASE URL CONNECTION THRU OPENWEBUI
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
import os
import uvicorn
import asyncio
import concurrent.futures
import json

# Import these from your main module
from paperqa import Settings, ask
from paperqa.settings import AgentSettings

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Remote Ollama configuration with your server IP
remote_ollama_base = "http://10.15.36.61:4107"

# Updated ollama config for both embedding and LLM
ollama_config = {
    "model_list": [
        {
            "model_name": "ollama/mxbai-embed-large",
            "litellm_params": {
                "model": "ollama/mxbai-embed-large",
                "api_base": remote_ollama_base,
            }
        },
        {
            "model_name": "ollama/llama3",
            "litellm_params": {
                "model": "ollama/llama3",
                "api_base": remote_ollama_base,
            }
        }
    ]
}

# Create a thread pool executor
executor = concurrent.futures.ThreadPoolExecutor()


def extract_answer_from_response(response_obj):
    """
    Extract the clean answer from the response object.
    """
    try:
        # First try to access the session object
        if hasattr(response_obj, 'session'):
            if hasattr(response_obj.session, 'formatted_answer'):
                return response_obj.session.formatted_answer
            elif hasattr(response_obj.session, 'answer'):
                return response_obj.session.answer

        # If the response is a dictionary or has __dict__ attribute
        if hasattr(response_obj, '__dict__'):
            obj_dict = response_obj.__dict__

            # Try to find session in the dictionary
            if 'session' in obj_dict:
                session = obj_dict['session']
                if hasattr(session, 'formatted_answer'):
                    return session.formatted_answer
                elif hasattr(session, 'answer'):
                    return session.answer
                elif isinstance(session, dict) and 'formatted_answer' in session:
                    return session['formatted_answer']
                elif isinstance(session, dict) and 'answer' in session:
                    return session['answer']

            # Try other common fields
            if 'formatted_answer' in obj_dict:
                return obj_dict['formatted_answer']
            elif 'answer' in obj_dict:
                return obj_dict['answer']

        # If it's a string, return it directly
        if isinstance(response_obj, str):
            return response_obj

        # If we can't find any specific answer field, convert the whole object to string
        return str(response_obj)

    except Exception as e:
        return f"Error extracting answer: {str(e)}"


def run_ask_function(query: str) -> Dict[str, Any]:
    """
    Run the ask function in a separate thread and return the result.
    This avoids event loop issues.
    """
    try:
        # Create settings with ollama/llama3 instead of Gemini
        settings = Settings(
            llm="ollama/llama3",
            llm_config=ollama_config,
            summary_llm="ollama/llama3",
            summary_llm_config=ollama_config,
            agent=AgentSettings(
                agent_llm="ollama/llama3",
                agent_llm_config=ollama_config
            ),
            embedding="ollama/mxbai-embed-large",
            embedding_config=ollama_config,
            verbosity=0
        )

        # Process the query
        answer_response = ask(
            query=query,
            settings=settings
        )

        # Extract just the clean answer from the complex response object
        clean_answer = extract_answer_from_response(answer_response)

        # Return the clean answer
        return {"answer": clean_answer}

    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


@app.get("/ask")
async def ask_question(q: str = Query(..., description="The question to ask")):
    """
    Ask a question via GET request and get a clean, user-friendly answer.
    """
    # Submit the task to the thread pool
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, run_ask_function, q)

    return result


if __name__ == "__main__":
    uvicorn.run("gemini_config_api:app", host="0.0.0.0", port=5555, reload=True)