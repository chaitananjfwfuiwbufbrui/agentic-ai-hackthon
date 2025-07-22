import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv

def get_lc_chat_history(messages):
    """Convert Streamlit chat messages (role: user/assistant) to LangChain format."""
    history = []
    for msg in messages:
        role = "human" if msg["role"] == "user" else "ai"
        history.append((role, msg["content"]))
    return history

def run_teacher_agent_chatbot():
    # Load .env only if not already loaded (idempotent)
    load_dotenv(".env", override=False)
    os.environ["GOOGLE_API_KEY"] = os.environ['GOOGLE_API_KEY']
    os.environ["SERPER_API_KEY"] = os.environ['SERPER_API_KEY']

    SYSTEM_PROMPT = (
        "You are an AI assistant for Indian school teachers. "
        "Reply in the user's chosen language, provide curriculum-relevant help, and use Indian contexts and examples. "
        "If asked for recent or factual information, use the web search tool."
        "if asked for english words but meaning in thier own language do it"
        
    )

    search = GoogleSerperAPIWrapper()

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2,
        max_tokens=2048
    )

    search_tool = Tool(
        name="Intermediate_Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )

    agent = initialize_agent(
        tools=[search_tool],
        llm=llm,
        agent="chat-conversational-react-description",
        verbose=False,
        system_prompt=SYSTEM_PROMPT
    )

   
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display message history
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_lang = st.selectbox(
        "Choose your language", 
        ["English", "Hindi", "Tamil", "Bengali", "Marathi", "Telugu", "Gujarati"]
    )
    user_prompt = st.chat_input("Type your message...")

    if user_prompt:
        prefix = f"(Please respond in {user_lang})\n"
        st.chat_message("user").markdown(user_prompt)
        st.session_state["messages"].append({"role": "user", "content": user_prompt})
        with st.spinner("Assistant typing..."):
            lc_history = get_lc_chat_history(st.session_state["messages"])
            output = agent.run({
                "input": prefix + user_prompt,
                "chat_history": lc_history
            })
        st.chat_message("assistant").markdown(output)
        st.session_state["messages"].append({"role": "assistant", "content": output})
