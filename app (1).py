import json
import os

import streamlit as st

from service_desk import DailyRequestLimit, MODEL, ServiceDeskError, generate_reply


MAX_MESSAGE_CHARS = 2000
MAX_STORED_MESSAGES = 40


@st.cache_resource
def request_limit():
    return DailyRequestLimit(50)


def get_api_key():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    try:
        return str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except FileNotFoundError:
        return ""


def display_reply(text, triage):
    if triage:
        st.json(json.loads(text), expanded=True)
    else:
        st.markdown(text)


st.set_page_config(page_title="AI Service Desk", page_icon="🛠️")
st.title("AI Service Desk")
st.caption("Troubleshoot IT issues or turn a ticket into a structured triage result.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "tokens" not in st.session_state:
    st.session_state.tokens = None

with st.sidebar:
    st.header("Chat settings")
    mode = st.radio("Mode", ("Support chat", "Ticket triage"))
    preferences = st.text_area(
        "Custom instructions",
        placeholder="Example: Use beginner-friendly language.",
        max_chars=500,
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.tokens = None
    st.caption(f"Model: {MODEL}")
    if st.session_state.tokens:
        input_tokens, total_tokens = st.session_state.tokens
        if input_tokens is not None:
            st.caption(f"Last reply input tokens: {input_tokens:,}")
        if total_tokens is not None:
            st.caption(f"Last reply total tokens: {total_tokens:,}")

api_key = get_api_key()
if not api_key:
    st.info("The app owner needs to configure GEMINI_API_KEY to enable chat.")

st.caption("Use sample tickets. Keep passwords and personal data out of the chat.")
history = st.session_state.messages
if not history:
    st.markdown('**Try asking** “Several employees can’t connect to the office Wi-Fi. What should I check first?”')

for message in history:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.text(message["text"])
        else:
            display_reply(message["text"], message["triage"])

prompt = st.chat_input("Describe an IT issue or paste a sample ticket",
                       max_chars=MAX_MESSAGE_CHARS, disabled=not api_key)
if prompt and prompt.strip():
    prompt = prompt.strip()
    triage = mode == "Ticket triage"
    if not request_limit().reserve():
        st.error("This demo reached its daily request limit. Try again after midnight UTC.")
        st.stop()

    with st.chat_message("user"):
        st.text(prompt)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Contacting Gemini…"):
                reply, input_tokens, total_tokens = generate_reply(
                    api_key, history, prompt, preferences.strip(), triage, temperature
                )
        except ServiceDeskError as error:
            st.error(str(error))
        else:
            st.session_state.messages = [
                *history,
                {"role": "user", "text": prompt},
                {"role": "assistant", "text": reply, "triage": triage},
            ][-MAX_STORED_MESSAGES:]
            st.session_state.tokens = (input_tokens, total_tokens)
            st.rerun()
