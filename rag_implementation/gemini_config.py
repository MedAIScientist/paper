# from paperqa import Settings, ask
# from paperqa.settings import AgentSettings
#
# # Configure Gemini API key in LiteLLM config
# gemini_config = {
#     "api_key": "AIzaSyBROcivtx7bzp2bbdU-x8ZJz6H8GhCaEkM",  # Put your actual API key here
#     "model_list": [
#         {
#             "model_name": "gemini/gemini-2.0-flash",
#             "litellm_params": {
#                 "model": "gemini/gemini-2.0-flash",
#                 "api_key": "AIzaSyBROcivtx7bzp2bbdU-x8ZJz6H8GhCaEkM"  # Put your actual API key here
#             }
#         }
#     ]
# }
#
# # Ollama config remains the same
# ollama_config = {
#     "model_list": [
#         {
#             "model_name": "ollama/mxbai-embed-large",
#             "litellm_params": {
#                 "model": "ollama/mxbai-embed-large",
#                 "api_base": "http://localhost:11434",
#             }
#         }
#     ]
# }
#
# # Use both configs
# answer_response = ask(
#     "griaffes fingerprint resemble with humans?",
#     settings=Settings(
#         llm="gemini/gemini-2.0-flash",
#         llm_config=gemini_config,
#         summary_llm="gemini/gemini-2.0-flash",
#         summary_llm_config=gemini_config,
#         agent=AgentSettings(
#             agent_llm="gemini/gemini-2.0-flash",
#             agent_llm_config=gemini_config
#         ),
#         embedding="ollama/mxbai-embed-large",
#         embedding_config=ollama_config
#     ),
# )
#
#
## //////////////////////////////////////////////
import os
import json
from paperqa import Settings, ask
from paperqa.settings import AgentSettings

# Disable OpenAI by removing its API key from environment
# if "OPENAI_API_KEY" in os.environ:
#     del os.environ["OPENAI_API_KEY"]
#
# # Add a mock OpenAI key that will cause errors if somehow OpenAI is still attempted
# os.environ["OPENAI_API_KEY"] = "INVALID_KEY_TO_PREVENT_OPENAI_USAGE"

# Configure Gemini API key in LiteLLM config
gemini_config = {
    "api_key": "AIzaSyBROcivtx7bzp2bbdU-x8ZJz6H8GhCaEkM",
    "model_list": [
        {
            "model_name": "gemini/ggemini-2.5-flash-preview-04-17",
            "litellm_params": {
                "model": "gemini/gemini-2.5-flash-preview-04-17",
                "api_key": "AIzaSyBROcivtx7bzp2bbdU-x8ZJz6H8GhCaEkM"
            }
        }
    ]
}

# Ollama config remains the same
ollama_config = {
    "model_list": [
        {
            "model_name": "ollama/mxbai-embed-large",
            "litellm_params": {
                "model": "ollama/mxbai-embed-large",
                "api_base": "http://localhost:11434",
            }
        }
    ]
}

# Create settings with increased verbosity to debug model usage
settings = Settings(
    # Set models to Gemini
    llm="gemini/gemini-2.5-flash-preview-04-17",
    llm_config=gemini_config,
    summary_llm="gemini/gemini-2.5-flash-preview-04-17",
    summary_llm_config=gemini_config,
    agent=AgentSettings(
        agent_llm="gemini/gemini-2.5-flash-preview-04-17",
        agent_llm_config=gemini_config
    ),
    # Set embedding to Ollama
    embedding="ollama/mxbai-embed-large",
    embedding_config=ollama_config,
    # Add verbose logging
    verbosity=0
)

# Optional: Print confirmation before running
print("Configuration secured against OpenAI usage.")
print(f"Using LLM: {settings.llm}")
print(f"Using embedding: {settings.embedding}")

try:
    # Use both configs
    user_query= input("Enter your query: ")
    answer_response = ask(
        query=user_query,
        settings=settings
    )

    print("\n--- FINAL ANSWER ---")
    # Fix the attribute access - the answer is in "answer" not "formatted_answer"
    print(answer_response.answer)

except Exception as e:
    if "INVALID_KEY_TO_PREVENT_OPENAI_USAGE" in str(e):
        print("OpenAI was attempted to be used despite configuration! Check your settings.")
    else:
        print(f"Error: {e}")

    # Print additional debugging info
    print("\nDebug information:")
    print(f"GEMINI_API_KEY set: {'GEMINI_API_KEY' in os.environ}")
    print(f"GOOGLE_API_KEY set: {'GOOGLE_API_KEY' in os.environ}")

##/***************************

# import os
# import json
# import re
# from paperqa import Settings, ask
# from paperqa.settings import AgentSettings
#
# # Disable OpenAI by removing its API key from environment
# if "OPENAI_API_KEY" in os.environ:
#     del os.environ["OPENAI_API_KEY"]
#
# # Add a mock OpenAI key that will cause errors if somehow OpenAI is still attempted
# os.environ["OPENAI_API_KEY"] = "INVALID_KEY_TO_PREVENT_OPENAI_USAGE"
#
# # Configure Gemini API key in LiteLLM config
# gemini_config = {
#     "api_key": "AIzaSyBROcivtx7bzp2bbdU-x8ZJz6H8GhCaEkM",
#     "model_list": [
#         {
#             "model_name": "gemini/ggemini-2.5-flash-preview-04-17",
#             "litellm_params": {
#                 "model": "gemini/gemini-2.5-flash-preview-04-17",
#                 "api_key": "AIzaSyBROcivtx7bzp2bbdU-x8ZJz6H8GhCaEkM"
#             }
#         }
#     ]
# }
#
# # Ollama config remains the same
# ollama_config = {
#     "model_list": [
#         {
#             "model_name": "ollama/mxbai-embed-large",
#             "litellm_params": {
#                 "model": "ollama/mxbai-embed-large",
#                 "api_base": "http://localhost:11434",
#             }
#         }
#     ]
# }
#
#
# def extract_answer_from_response(response_text):
#     """
#     Extract the answer section from the PaperQA verbose output.
#     This function handles both formatted console output and direct response objects.
#     """
#     # If we have a response object with an answer attribute
#     if hasattr(response_text, 'answer'):
#         return response_text.answer.strip()
#
#     # For string output (when capturing stdout or logs)
#     if isinstance(response_text, str):
#         # Look for the Answer: section at the end of the output
#         answer_pattern = r"Answer:\s*(.*?)(?=\n\n|\Z)"
#         matches = re.findall(answer_pattern, response_text, re.DOTALL)
#
#         if matches:
#             # Get the last match (in case there are multiple "Answer:" sections)
#             answer = matches[-1].strip()
#             # Clean up any line breaks and extra whitespace for readability
#             answer = re.sub(r'\s+', ' ', answer)
#             return answer
#
#     # If nothing works, return an error message
#     return "Could not extract answer from response"
#
#
# # Create settings with increased verbosity to debug model usage
# settings = Settings(
#     # Set models to Gemini
#     llm="gemini/gemini-2.5-flash-preview-04-17",
#     llm_config=gemini_config,
#     summary_llm="gemini/gemini-2.5-flash-preview-04-17",
#     summary_llm_config=gemini_config,
#     agent=AgentSettings(
#         agent_llm="gemini/gemini-2.5-flash-preview-04-17",
#         agent_llm_config=gemini_config
#     ),
#     # Set embedding to Ollama
#     embedding="ollama/mxbai-embed-large",
#     embedding_config=ollama_config,
#     # Add verbose logging
#     verbosity=2
# )
#
# # Optional: Print confirmation before running
# print("Configuration secured against OpenAI usage.")
# print(f"Using LLM: {settings.llm}")
# print(f"Using embedding: {settings.embedding}")
#
# try:
#     # Capture the raw output if needed for debugging
#     full_response = ask(
#         "current threats for giraffes",
#         settings=settings
#     )
#
#     # Extract just the answer part
#     clean_answer = None
#
#     # Try various ways to get the answer based on the response structure
#     if hasattr(full_response, 'answer'):
#         clean_answer = full_response.answer
#     elif hasattr(full_response, 'formatted_answer'):
#         clean_answer = extract_answer_from_response(full_response.formatted_answer)
#     elif hasattr(full_response, 'agent_response'):
#         if hasattr(full_response.agent_response, 'answer'):
#             clean_answer = full_response.agent_response.answer
#
#     # If all else fails, try to extract from string representation
#     if not clean_answer:
#         clean_answer = extract_answer_from_response(str(full_response))
#
#     print("\n--- CLEAN ANSWER ---")
#     print(clean_answer)
#
# except Exception as e:
#     if "INVALID_KEY_TO_PREVENT_OPENAI_USAGE" in str(e):
#         print("OpenAI was attempted to be used despite configuration! Check your settings.")
#     else:
#         print(f"Error: {e}")
#
#     # Print additional debugging info
#     print("\nDebug information:")
#     print(f"GEMINI_API_KEY set: {'GEMINI_API_KEY' in os.environ}")
#     print(f"GOOGLE_API_KEY set: {'GOOGLE_API_KEY' in os.environ}")