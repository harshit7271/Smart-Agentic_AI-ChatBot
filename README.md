# Smart-Agentic_AI-ChatBot

This repository contains a Streamlit-based AI chatbot application powered by LangChain's Groq integration and Tavily search tools.

## Demo
Check out the live demo here: [Personal AI Agent Chatbot 🚀
](https://smart-agenticai-chatbot-9odt34hobsn2z8gwhxnhmu.streamlit.app/)

---

## Features

- Conversational AI chatbot with dynamic LLM from Groq (Llama 3.3 70B versatile model by default)
- Integrated smart search capability using TavilySearchResults tool
- Interactive chat UI built with Streamlit and FastAPI for scaling
- Supports customizable system prompts and search toggling
- Secure API key management using environment variables

---

### Prerequisites

- Python 3.8+
- Groq API key (sign up at Groq and get your API key)
- (Optional) Tavily API key for search tool usage

### Installation

1. Clone the repo:
```bash
https://github.com/harshit7271/Smart-Agentic_AI-ChatBot.git
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following:

```bash
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```


---

## Usage

Run the Streamlit app locally with:

```bash
streamlit run app.py
```

- Enter your message and interact with the AI chatbot.
- Customize the system prompt, choose model and toggle search in the sidebar.

---

## Code Highlights

- Loads API keys securely via `python-dotenv`.
- Initializes `ChatGroq` LLM with the Groq API key.
- Uses `create_react_agent` from `langgraph` to build the agent.
- Handles chat history in Streamlit's session state.
- Displays alternating user and AI messages.
- Includes social media icons and footer branding.

---

## Deployment

- Ensure the environment variables `GROQ_API_KEY` and `TAVILY_API_KEY` are set on your hosting platform.
- Streamlit cloud or Render support environment variable configuration.
- Avoid committing `.env` to GitHub.
  
---

## Dependencies (`requirements.txt`)
```bash
streamlit
python-dotenv
langchain-groq
langchain-community
langgraph
langchain-core
tavily-python
requests
st-social-media-links
pydantic
fastapi
uvicorn
pydantic
```

Created by Harshit™



 
