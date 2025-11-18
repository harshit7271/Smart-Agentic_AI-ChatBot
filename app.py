import streamlit as st
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

# Load environment variables locally
load_dotenv()

# Load API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize LLM and Search Tool
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider="Groq"):
    if provider != "Groq":
        raise ValueError("Currently only 'Groq' provider is supported.")
    
    llm = ChatGroq(model=llm_id)
    search_tool = TavilySearchResults(max_results=2)

    agent = create_react_agent(
        model=llm,
        tools=[search_tool] if allow_search else [],
        prompt=system_prompt
    )

    response = agent.invoke({"messages": [{"role": "user", "content": query}]})
    messages = response.get("messages") or []
    
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
    if not ai_messages:
        raise RuntimeError("No response from AI agent")

    return ai_messages[-1]


st.title("Personal AI Agent Chatbot")

# Sidebar inputs
model_name = st.sidebar.text_input("Model from which you getting information", "llama-3.3-70b-versatile")
model_provider = st.sidebar.text_input("Model Provider", "Groq")
system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="Act as an AI chatbot who is smart and friendly"
)
allow_search = st.sidebar.checkbox("Allow Search", True)

# Text input for user
user_message = st.text_input("Enter your message or queries")

# Session state to hold chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Send"):
    if user_message.strip() == "":
        st.warning("Please enter a message.")
    else:
        st.session_state.messages.append(user_message)
        try:
            reply = get_response_from_ai_agent(
                llm_id=model_name,
                query=user_message,
                allow_search=allow_search,
                system_prompt=system_prompt,
                provider=model_provider
            )
            st.session_state.messages.append(reply)
        except Exception as e:
            st.error(f"Error: {e}")

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    if i % 2 == 0:
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**AI:** {msg}")

# social links and footer remain unchanged below
from st_social_media_links import SocialMediaIcons
social_media_links = [
    "https://github.com/harshit7271",
    "https://www.linkedin.com/in/harshit-singh-40b390286/",
    "https://x.com/HarshitSin12380"
]
social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()

footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f0f0f0;
    color: #555;
    text-align: center;
    padding: 5px 0;
    font-size: 12px;
    font-family: Arial, sans-serif;
}
</style>

<div class="footer">
    Created by Harshit&#8482;
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
