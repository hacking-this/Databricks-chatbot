from datetime import datetime
import streamlit as st
from scripts.chatbot import get_response

st.set_page_config(page_title="Databricks Chatbot", page_icon="🧠")

st.title("🧠 Databricks Chatbot")
st.markdown("Ask me anything about Databricks, and I’ll generate relevant info and code!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "archive_chat_index" not in st.session_state:
    st.session_state.archive_chat_index = None

# --- SIDEBAR: LOAD OR START NEW CHAT ---
with st.sidebar:
    st.sidebar.header("🗂️ Previous Chats")
    for i, chat in enumerate(st.session_state.chat_sessions):
        if st.button(chat["title"], key=f"chat_{i}"):
            st.session_state.messages = chat["messages"].copy()
            st.session_state.chat_history = chat["chat_history"].copy()
            st.session_state.archive_chat_index = i

    st.markdown("---")
    if st.button("🆕 New Chat"):
        # Archive current chat before resetting
        if st.session_state.messages:
            title = st.session_state.messages[0]["content"][:40] if st.session_state.messages else "New Chat"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            session = {
                "title": f"{title} ({timestamp})",
                "messages": st.session_state.messages.copy(),
                "history": st.session_state.chat_history.copy()
            }
            st.session_state.chat_sessions.append(session)

        # Clear for new chat
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.active_chat_index = None

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
user_input = st.chat_input("Ask your question here...")

if user_input:
    # Display user message in chat
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append(("User", user_input))

    # Generate response
    response = get_response(user_input, st.session_state.chat_history)
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.chat_history.append(("Assistant", response))


