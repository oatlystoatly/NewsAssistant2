
import streamlit as st
from bob_bot import BobBot

st.set_page_config(page_title="Bob Bot")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #e8f5e9;
    }

    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background-color: #dcedc8;
        border-radius: 12px;
        padding: 0.75rem;
    }

    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background-color: #dbeafe;
        border-radius: 12px;
        padding: 0.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Bob Bot")
st.caption("Personalised intelligent assistant :-)")

# Preserve the chatbot between interactions
if "bot" not in st.session_state:
    st.session_state.bot = BobBot()
    st.session_state.bot.say(
        "Hello! How can I assist you today?"
    )

bot = st.session_state.bot
if "show_history" not in st.session_state:
    st.session_state.show_history = False

# Display conversation history
for role, message in bot.history:
    chat_role = "user" if role == "You" else "assistant"

    with st.chat_message(chat_role):
        st.text(message)

if st.session_state.show_history:
    with st.expander("Conversation history", expanded=True):
        for role, message in bot.history:
            if role == "Bob Bot" and message.startswith("Session transcript:\n"):
                continue
            st.write(f"{role}: {message}")

# Accept new messages
if prompt := st.chat_input("Ask Bob Bot..."):
    bot.handle(prompt)
    st.session_state.show_history = prompt.strip().casefold() == "history"
    st.rerun()
