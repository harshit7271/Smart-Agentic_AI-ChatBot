import streamlit as st
import requests

st.title("Personal AI Agent Chatbot")

API_URL = "https://smart-agentic-ai-chatbot-1.onrender.com/chat"

# Sidebar 
model_name = st.sidebar.text_input("Model from which you getting information", "llama-3.3-70b-versatile")
model_provider = st.sidebar.text_input("Model Provider", "Groq")

system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="Act as an AI chatbot who is smart and friendly"
)

allow_search = st.sidebar.checkbox("Allow Search", True)

# Text input
user_message = st.text_input("Enter your message or querries")

# Maintain chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# send request to FastAPI backend by clicking on send button
if st.button("Send"):
    if user_message.strip() == "":
        st.warning("Please enter a message.")
    else:
        # Append user message to session state
        st.session_state.messages.append(user_message)
        
        # JSON payload for FastAPI
        payload = {
            "model_name": model_name,
            "model_provider": model_provider,
            "system_prompt": system_prompt,
            "messages": st.session_state.messages,
            "allow_search": allow_search
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            ai_reply = data.get("reply", "(No response)")
            # Append AI reply to chat history
            st.session_state.messages.append(ai_reply)
        except Exception as e:
            st.error(f"Error: {e}")

# Display chat history as alternating messages
for i, msg in enumerate(st.session_state.messages):
    if i % 2 == 0:
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**AI:** {msg}")


# adding my details 

st.markdown("---")
from st_social_media_links import SocialMediaIcons
# Social media links list
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




