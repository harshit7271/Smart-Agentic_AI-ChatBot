from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Import your AI components
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

# Load API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Allowed model names for validation
ALLOWED_MODEL_NAMES = ["llama-3.3-70b-versatile", "llama3-70b-8192"]

# Define Pydantic model for request validation
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

app = FastAPI(title="LangGraph AI Agent")

@app.get("/")
def root():
    return {"message": "Welcome to AI agent ChatBot backend"}


@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API endpoint to interact with the chatbot using LangGraph and search tools.
    Dynamically selects the model and controls search tool usage.
    """
    # Validate model name
    if request.model_name not in ALLOWED_MODEL_NAMES:
        raise HTTPException(status_code=400, detail="Invalid model name. Kindly select a valid AI model.")

    # Currently only Groq provider supported
    if request.model_provider.lower() != "groq":
        raise HTTPException(status_code=400, detail="Only 'Groq' model provider is supported currently.")

    # Initialize the LLM with the requested model name and API key
    llm = ChatGroq(model=request.model_name)

    # Initialize the search tool if allowed
    tools = [TavilySearchResults(max_results=2)] if request.allow_search else []

    # Create the AI agent with system prompt and tools
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=request.system_prompt
    )

    # Prepare messages for the agent (assume all user messages)
    message_objs = [{"role": "user", "content": msg} for msg in request.messages]

    # Invoke the agent
    response = agent.invoke({"messages": message_objs})

    messages = response.get("messages") or []
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
    if not ai_messages:
        raise HTTPException(status_code=500, detail="No response from AI agent.")

    # Return the last AI message as response
    return {"reply": ai_messages[-1]}

