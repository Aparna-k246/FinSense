import streamlit as st
import requests
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BACKEND_URL = "https://finsense-production-b33a.up.railway.app"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="FinSense", page_icon="💰")

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def show_auth_page():
    st.title("💰 FinSense")
    st.caption("Your AI financial decision coach")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Welcome back")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", use_container_width=True):
            try:
                response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                st.session_state.user = response.user
                st.session_state.messages = []
                st.rerun()
            except Exception as e:
                st.error("Invalid email or password. Please try again.")

    with tab2:
        st.subheader("Create your account")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input(
            "Password (min 6 characters)", 
            type="password", 
            key="signup_password"
        )
        
        if st.button("Sign Up", use_container_width=True):
            try:
                response = supabase.auth.sign_up({
                    "email": new_email,
                    "password": new_password
                })
                st.success("Account created! Please check your email to verify, then login.")
            except Exception as e:
                st.error("Sign up failed. Please try again.")

def show_chat_page():
    # Header with logout
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("💰 FinSense")
        st.caption("Your AI financial decision coach")
    with col2:
        if st.button("Logout"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask FinSense anything about your finances..."):
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt
        })
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call backend with user's actual ID from Supabase Auth
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "user_id": st.session_state.user.id,
                "message": prompt
            }
        )

        reply = response.json()["reply"]
        st.session_state.messages.append({
            "role": "assistant", 
            "content": reply
        })
        with st.chat_message("assistant"):
            st.markdown(reply)

# Route to correct page
if st.session_state.user is None:
    show_auth_page()
else:
    show_chat_page()