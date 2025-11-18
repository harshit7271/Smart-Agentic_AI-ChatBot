from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()  # Load environment variables from .env

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

# Load API keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Validate API key presence
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY environment variable is missing. Please set it before running.")

# Initialize global LLM instance with API key
groq_llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
search_tool = TavilySearchResults(max_results=2)

system_prompt = "Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider="Groq"):
    if provider.lower() != "groq":
        raise ValueError("Currently only 'Groq' model provider is supported.")
    
    # Use the pre-initialized groq_llm; or optionally create per-call if dynamic models needed
    agent = create_react_agent(
        model=groq_llm,
        tools=[search_tool] if allow_search else [],
        prompt=system_prompt
    )

    response = agent.invoke({"messages": [{"role": "user", "content": query}]})
    messages = response.get



