from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

# Load API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize LLM and Search Tool
groq_llm = ChatGroq(model="llama-3.3-70b-versatile",  api_key=GROQ_API_KEY)
search_tool = TavilySearchResults(max_results=2)

system_prompt = "Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider="Groq"):
    if provider != "Groq":
        raise ValueError("Currently only 'Groq' provider is supported.")
    
    # You can optionally recreate llm here using llm_id if needed, or use the pre-initialized one
    # llm = ChatGroq(model=llm_id, api_key=GROQ_API_KEY)
    agent = create_react_agent(
        model=groq_llm,
        tools=[search_tool] if allow_search else [],
        prompt=system_prompt
    )

    response = agent.invoke({"messages": [{"role": "user", "content": query}]})
    messages = response.get("messages") or []
    
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
    if not ai_messages:
        raise RuntimeError("No response from AI agent")

    return ai_messages[-1]

# Example usage:
if __name__ == "__main__":
    test_query = "Tell me about the trends in crypto markets"
    reply = get_response_from_ai_agent("llama-3.3-70b-versatile", test_query, allow_search=True, system_prompt=system_prompt)
    print(reply)



