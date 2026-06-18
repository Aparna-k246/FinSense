import streamlit as st
import requests
import uuid

st.set_page_config(page_title="FinSense", page_icon="💰")
st.title("💰 FinSense")
st.caption("Your AI financial decision coach")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if not st.session_state.user_id:
    st.markdown("### Welcome to FinSense 💰")
    st.markdown("Your personal AI financial coach for smarter money decisions.")
    name = st.text_input("Enter your name to get started:")
    if st.button("Start") and name.strip():
        st.session_state.user_id = "user_" + name.strip().lower().replace(" ", "_")
        st.rerun()
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask FinSense anything about your finances..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(
        "https://finsense-production-183b.up.railway.app/chat",
        json={
            "user_id": st.session_state.user_id,
            "message": prompt
        }
    )

    reply = response.json()["reply"]
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)