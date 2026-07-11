import streamlit as st
import requests
from supabase import create_client
import os

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
BACKEND_URL = "https://finsense-production-b33a.up.railway.app"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(
    page_title="FinSense",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============ CUSTOM CSS ============

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0A0F1E;
    color: #E8EDF5;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; }

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: none !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6B7A99 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(74,222,128,0.12) !important;
    color: #4ADE80 !important;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #E8EDF5 !important;
    font-size: 0.9rem !important;
    padding: 12px 16px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #4ADE80 !important;
    box-shadow: 0 0 0 3px rgba(74,222,128,0.1) !important;
}

.stTextInput label {
    color: #A0AEBF !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #4ADE80, #22C55E) !important;
    color: #0A0F1E !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 12px 24px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(74,222,128,0.25) !important;
}

.stChatMessage {
    background: transparent !important;
    border: none !important;
}

[data-testid="stChatMessageContent"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    font-size: 0.9rem !important;
    line-height: 1.7 !important;
    color: #D4DCE8 !important;
}

.stChatInput textarea {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #E8EDF5 !important;
    font-size: 0.9rem !important;
}

.stAlert {
    border-radius: 10px !important;
    font-size: 0.85rem !important;
}

.profile-label {
    font-size: 0.7rem;
    color: #6B7A99;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
}

.profile-value {
    font-size: 0.9rem;
    color: #E8EDF5;
    font-weight: 500;
    margin-bottom: 12px;
}

.status-dot {
    width: 6px;
    height: 6px;
    background: #4ADE80;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

.logout-btn > button {
    background: rgba(255,255,255,0.06) !important;
    color: #6B7A99 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    font-size: 0.8rem !important;
}

.logout-btn > button:hover {
    background: rgba(255,80,80,0.1) !important;
    color: #FF6B6B !important;
    transform: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============

if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = None

# ============ AUTH PAGE ============

def show_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; margin-bottom:32px; margin-top:40px;">
            <div style="font-family:'DM Serif Display',serif; font-size:2.4rem;
            color:#FFFFFF; letter-spacing:-0.02em;">
                Fin<span style="color:#4ADE80;">Sense</span>
            </div>
            <div style="font-size:0.85rem; color:#6B7A99; margin-top:8px;">
                Your AI financial decision coach
            </div>
            <div style="margin-top:8px; font-size:0.78rem; color:#4B5563;
            font-style:italic;">
                Built for young Indian professionals
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            st.markdown("<div style='height:8px'></div>",
                        unsafe_allow_html=True)
            email = st.text_input("Email address", key="login_email",
                                  placeholder="you@example.com")
            password = st.text_input("Password", type="password",
                                     key="login_password",
                                     placeholder="••••••••")
            st.markdown("<div style='height:8px'></div>",
                        unsafe_allow_html=True)

            if st.button("Sign in to FinSense", use_container_width=True,
                         key="login_btn"):
                if not email or not password:
                    st.error("Please enter your email and password.")
                else:
                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        st.session_state.user = response.user
                        st.session_state.messages = []
                        st.rerun()
                    except Exception as e:
                        error_msg = str(e).lower()
                        if "invalid" in error_msg or "credentials" in error_msg:
                            st.error("Wrong email or password. Please try again.")
                        elif "confirm" in error_msg:
                            st.warning("Please verify your email before logging in.")
                        else:
                            st.error("Login failed. Please try again.")

        with tab2:
            st.markdown("<div style='height:8px'></div>",
                        unsafe_allow_html=True)
            new_email = st.text_input("Email address", key="signup_email",
                                      placeholder="you@example.com")
            new_password = st.text_input("Password", type="password",
                                         key="signup_password",
                                         placeholder="At least 6 characters")
            st.markdown("<div style='height:8px'></div>",
                        unsafe_allow_html=True)

            if st.button("Create account", use_container_width=True,
                         key="signup_btn"):
                if not new_email or not new_password:
                    st.error("Please enter both email and password.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    try:
                        response = supabase.auth.sign_up({
                            "email": new_email,
                            "password": new_password
                        })
                        st.success("Account created! You can now log in.")
                    except Exception as e:
                        error_msg = str(e).lower()
                        if "already registered" in error_msg or "already exists" in error_msg:
                            st.error("This email is already registered. Please log in instead.")
                        elif "invalid email" in error_msg:
                            st.error("Please enter a valid email address.")
                        else:
                            st.error("Sign up failed. Please try again.")

        st.markdown("""
        <div style="margin-top:24px; text-align:center;">
            <div style="font-size:0.72rem; color:#374151; line-height:1.6;">
                FinSense does not provide SEBI-registered financial advice.<br>
                Always verify important decisions with a qualified advisor.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============ PROFILE FETCH ============

def fetch_profile(user_id: str):
    try:
        response = requests.get(
            f"{BACKEND_URL}/profile/{user_id}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "message" not in data:
                return data
    except Exception:
        pass
    return None

# ============ CHAT PAGE ============

def show_chat_page():
    user = st.session_state.user

    if st.session_state.profile is None:
        st.session_state.profile = fetch_profile(user.id)

    profile = st.session_state.profile

    # ── Sidebar ──
    with st.sidebar:
        st.markdown("""
        <div style="font-family:'DM Serif Display',serif; font-size:1.4rem;
        color:#FFFFFF; margin-bottom:4px;">
            Fin<span style="color:#4ADE80;">Sense</span>
        </div>
        <div style="font-size:0.75rem; color:#6B7A99; margin-bottom:20px;">
            AI Financial Coach
        </div>
        <hr style="border-color:rgba(255,255,255,0.06); margin-bottom:20px;">
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="profile-label">Signed in as</div>
        <div class="profile-value" style="font-size:0.82rem;
        word-break:break-all;">{user.email}</div>
        """, unsafe_allow_html=True)

        if profile:
            st.markdown("""
            <div style="font-size:0.72rem; color:#6B7A99;
            text-transform:uppercase; letter-spacing:0.06em;
            margin:16px 0 12px;">Your profile</div>
            """, unsafe_allow_html=True)

            fields = {
                "Monthly income": profile.get("monthly_income"),
                "Fixed expenses": profile.get("fixed_expenses"),
                "EMI": profile.get("emi_amount"),
                "Investments": profile.get("existing_investments"),
                "Goals": profile.get("financial_goals"),
                "Concern": profile.get("biggest_worry"),
            }

            for label, value in fields.items():
                if value and str(value) != "None":
                    display = f"₹{int(value):,}" if isinstance(
                        value, (int, float)) else str(value)
                    st.markdown(f"""
                    <div class="profile-label">{label}</div>
                    <div class="profile-value">{display}</div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(74,222,128,0.06);
            border:1px solid rgba(74,222,128,0.15);
            border-radius:10px; padding:12px; margin:16px 0;">
                <div style="font-size:0.78rem; color:#4ADE80;
                font-weight:600; margin-bottom:4px;">💡 Auto profile</div>
                <div style="font-size:0.74rem; color:#6B7A99;
                line-height:1.5;">Share your income in chat —
                FinSense remembers it automatically.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>",
                    unsafe_allow_html=True)

        if st.button("Clear conversation", use_container_width=True,
                     key="clear_btn"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("<div style='height:8px'></div>",
                    unsafe_allow_html=True)

        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("Sign out", use_container_width=True,
                     key="logout_btn"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.session_state.messages = []
            st.session_state.profile = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:24px; font-size:0.7rem;
        color:#374151; line-height:1.5;">
            Not SEBI-registered advice.<br>
            Verify with a qualified advisor.
        </div>
        """, unsafe_allow_html=True)

    # ── Header ──
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("""
        <div style="padding:16px 0 8px;">
            <span style="font-family:'DM Serif Display',serif;
            font-size:1.6rem; color:#FFFFFF;">
                Fin<span style="color:#4ADE80;">Sense</span>
            </span>
            <span style="margin-left:10px; font-size:0.75rem;
            color:#4ADE80;">
                <span class="status-dot"></span>Active
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.06); margin:0 0 16px;">
    """, unsafe_allow_html=True)

    # ── Empty state ──
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center; padding:40px 24px 24px;">
            <div style="font-size:2.5rem; margin-bottom:12px;">💬</div>
            <div style="font-family:'DM Serif Display',serif;
            font-size:1.5rem; color:#FFFFFF; margin-bottom:8px;">
                What's on your mind?
            </div>
            <div style="font-size:0.85rem; color:#6B7A99;
            line-height:1.6; max-width:340px; margin:0 auto 24px;">
                Ask me anything about your finances — from building
                an emergency fund to calculating your home loan EMI.
            </div>
        </div>
        """, unsafe_allow_html=True)

        suggestions = [
            "How much emergency fund do I need?",
            "Should I invest in SIP or FD?",
            "Calculate my home loan EMI",
            "I just got my first salary — what now?",
            "Help me plan my savings",
        ]

        cols = st.columns(3)
        for i, suggestion in enumerate(suggestions[:3]):
            with cols[i]:
                if st.button(suggestion, key=f"sug_{i}",
                             use_container_width=True):
                    st.session_state.messages.append(
                        {"role": "user", "content": suggestion})
                    with st.spinner("FinSense is thinking..."):
                        try:
                            resp = requests.post(
                                f"{BACKEND_URL}/chat",
                                json={"user_id": user.id,
                                      "message": suggestion},
                                timeout=60
                            )
                            reply = resp.json()["reply"]
                        except requests.exceptions.Timeout:
                            reply = "Taking longer than expected. Please try again."
                        except Exception:
                            reply = "Something went wrong. Please try again."
                    st.session_state.messages.append(
                        {"role": "assistant", "content": reply})
                    st.session_state.profile = fetch_profile(user.id)
                    st.rerun()

        cols2 = st.columns(2)
        for i, suggestion in enumerate(suggestions[3:]):
            with cols2[i]:
                if st.button(suggestion, key=f"sug_{i+3}",
                             use_container_width=True):
                    st.session_state.messages.append(
                        {"role": "user", "content": suggestion})
                    with st.spinner("FinSense is thinking..."):
                        try:
                            resp = requests.post(
                                f"{BACKEND_URL}/chat",
                                json={"user_id": user.id,
                                      "message": suggestion},
                                timeout=60
                            )
                            reply = resp.json()["reply"]
                        except requests.exceptions.Timeout:
                            reply = "Taking longer than expected. Please try again."
                        except Exception:
                            reply = "Something went wrong. Please try again."
                    st.session_state.messages.append(
                        {"role": "assistant", "content": reply})
                    st.session_state.profile = fetch_profile(user.id)
                    st.rerun()

    # ── Messages ──
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ── Input ──
    if prompt := st.chat_input("Ask about your finances..."):
        st.session_state.messages.append(
            {"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("FinSense is thinking..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/chat",
                        json={"user_id": user.id, "message": prompt},
                        timeout=60
                    )
                    reply = response.json()["reply"]
                except requests.exceptions.Timeout:
                    reply = "Taking longer than expected. Please try again."
                except Exception:
                    reply = "Something went wrong. Please try again."
            st.markdown(reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": reply})
        st.session_state.profile = fetch_profile(user.id)

# ============ ROUTER ============

if st.session_state.user is None:
    show_auth_page()
else:
    show_chat_page()