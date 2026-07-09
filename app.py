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

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0A0F1E;
    color: #E8EDF5;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Auth page ── */
.auth-wrapper {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #0A0F1E 0%, #0D1B3E 50%, #0A0F1E 100%);
}

.auth-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 48px 40px;
    width: 100%;
    max-width: 420px;
    backdrop-filter: blur(20px);
}

.brand-mark {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    line-height: 1;
}

.brand-accent {
    color: #4ADE80;
}

.brand-sub {
    font-size: 0.85rem;
    color: #6B7A99;
    margin-top: 4px;
    letter-spacing: 0.02em;
}

/* ── Streamlit tab override ── */
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

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #E8EDF5 !important;
    font-family: 'Inter', sans-serif !important;
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
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

/* ── Primary button ── */
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
    letter-spacing: 0.01em !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(74,222,128,0.25) !important;
}

/* ── Chat page header ── */
.chat-header {
    background: rgba(10,15,30,0.95);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(20px);
}

.chat-header-brand {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #FFFFFF;
}

.chat-header-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    color: #4ADE80;
}

.status-dot {
    width: 6px;
    height: 6px;
    background: #4ADE80;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Chat messages ── */
.stChatMessage {
    background: transparent !important;
    border: none !important;
    padding: 8px 24px !important;
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

[data-testid="stChatMessageContent"] p {
    margin: 0 0 8px 0 !important;
}

[data-testid="stChatMessageContent"] strong {
    color: #FFFFFF !important;
}

/* User message bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
    background: rgba(74,222,128,0.08) !important;
    border-color: rgba(74,222,128,0.15) !important;
    color: #E8EDF5 !important;
}

/* ── Chat input ── */
.stChatInput {
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    background: rgba(10,15,30,0.95) !important;
    padding: 16px 24px !important;
    backdrop-filter: blur(20px) !important;
}

.stChatInput textarea {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #E8EDF5 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}

.stChatInput textarea:focus {
    border-color: #4ADE80 !important;
    box-shadow: 0 0 0 3px rgba(74,222,128,0.08) !important;
}

/* ── Welcome chips ── */
.suggestion-chip {
    display: inline-block;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 0.8rem;
    color: #A0AEBF;
    margin: 4px;
    cursor: pointer;
    transition: all 0.2s;
}

.suggestion-chip:hover {
    border-color: #4ADE80;
    color: #4ADE80;
    background: rgba(74,222,128,0.06);
}

/* ── Sidebar / Profile panel ── */
.profile-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
}

.profile-label {
    font-size: 0.7rem;
    color: #6B7A99;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
}

.profile-value {
    font-size: 0.95rem;
    color: #E8EDF5;
    font-weight: 500;
}

/* ── Logout button override ── */
.logout-btn > button {
    background: rgba(255,255,255,0.06) !important;
    color: #6B7A99 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    font-size: 0.8rem !important;
    padding: 8px 16px !important;
    width: auto !important;
}

.logout-btn > button:hover {
    background: rgba(255,80,80,0.1) !important;
    color: #FF6B6B !important;
    border-color: rgba(255,80,80,0.2) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── Alert overrides ── */
.stAlert {
    border-radius: 10px !important;
    font-size: 0.85rem !important;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 60px 24px;
}

.empty-state-icon {
    font-size: 3rem;
    margin-bottom: 16px;
}

.empty-state-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: #FFFFFF;
    margin-bottom: 8px;
}

.empty-state-sub {
    font-size: 0.875rem;
    color: #6B7A99;
    line-height: 1.6;
    max-width: 320px;
    margin: 0 auto 24px;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 8px 0;
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
    st.markdown("""
    <div style="min-height:100vh; display:flex; align-items:center; 
    justify-content:center; padding:24px;">
    <div style="width:100%; max-width:420px;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-bottom:40px;">
        <div style="font-family:'DM Serif Display',serif; font-size:2.4rem; 
        color:#FFFFFF; letter-spacing:-0.02em;">
            Fin<span style="color:#4ADE80;">Sense</span>
        </div>
        <div style="font-size:0.85rem; color:#6B7A99; margin-top:8px;">
            Your AI financial decision coach
        </div>
        <div style="margin-top:16px; font-size:0.8rem; color:#4B5563; 
        font-style:italic;">
            Built for young Indian professionals
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        email = st.text_input("Email address", key="login_email",
                              placeholder="you@example.com")
        password = st.text_input("Password", type="password",
                                 key="login_password",
                                 placeholder="••••••••")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

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
                    elif "email" in error_msg and "confirm" in error_msg:
                        st.warning("Please verify your email before logging in.")
                    else:
                        st.error("Login failed. Please try again.")

    with tab2:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        new_email = st.text_input("Email address", key="signup_email",
                                  placeholder="you@example.com")
        new_password = st.text_input("Password", type="password",
                                     key="signup_password",
                                     placeholder="At least 6 characters")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

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
    <div style="margin-top:32px; text-align:center;">
        <div style="font-size:0.72rem; color:#374151; line-height:1.6;">
            FinSense does not provide SEBI-registered financial advice.<br>
            Always verify important decisions with a qualified advisor.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# ============ PROFILE FETCH ============

def fetch_profile(user_id: str):
    try:
        response = requests.get(f"{BACKEND_URL}/profile/{user_id}", timeout=5)
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

    # Fetch profile if not cached
    if st.session_state.profile is None:
        st.session_state.profile = fetch_profile(user.id)

    profile = st.session_state.profile

    # ── Sidebar ──
    with st.sidebar:
        st.markdown("""
        <div style="font-family:'DM Serif Display',serif; font-size:1.3rem; 
        color:#FFFFFF; margin-bottom:4px;">
            Fin<span style="color:#4ADE80;">Sense</span>
        </div>
        <div style="font-size:0.75rem; color:#6B7A99; margin-bottom:24px;">
            AI Financial Coach
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # User info
        st.markdown(f"""
        <div class="profile-label">Signed in as</div>
        <div class="profile-value" style="font-size:0.85rem; 
        word-break:break-all;">{user.email}</div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # Profile data if available
        if profile:
            st.markdown("""
            <div style="font-size:0.75rem; color:#6B7A99; 
            text-transform:uppercase; letter-spacing:0.06em; 
            margin-bottom:12px;">Your profile</div>
            """, unsafe_allow_html=True)

            fields = {
                "Monthly income": profile.get("monthly_income"),
                "Fixed expenses": profile.get("fixed_expenses"),
                "EMI amount": profile.get("emi_amount"),
                "Investments": profile.get("existing_investments"),
                "Goals": profile.get("financial_goals"),
                "Concern": profile.get("biggest_worry"),
            }

            for label, value in fields.items():
                if value and str(value) != "None":
                    display = f"₹{int(value):,}" if isinstance(value, (int, float)) else str(value)
                    st.markdown(f"""
                    <div style="margin-bottom:12px;">
                        <div class="profile-label">{label}</div>
                        <div class="profile-value" 
                        style="font-size:0.85rem;">{display}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(74,222,128,0.06); border:1px solid 
            rgba(74,222,128,0.15); border-radius:10px; padding:12px; 
            margin-bottom:16px;">
                <div style="font-size:0.78rem; color:#4ADE80; 
                font-weight:600; margin-bottom:4px;">💡 Profile building</div>
                <div style="font-size:0.75rem; color:#6B7A99; 
                line-height:1.5;">Share your income and expenses in chat — 
                FinSense will remember them automatically.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # Clear chat
        if st.button("Clear conversation", use_container_width=True,
                     key="clear_btn"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Logout
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("Sign out", use_container_width=True, key="logout_btn"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.session_state.messages = []
            st.session_state.profile = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="position:absolute; bottom:24px; left:24px; right:24px;">
            <div style="font-size:0.7rem; color:#374151; line-height:1.5;">
                Not SEBI-registered advice.<br>
                Verify decisions with a qualified advisor.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Main chat area ──
    st.markdown("""
    <div class="chat-header">
        <div style="display:flex; align-items:center; gap:12px;">
            <div class="chat-header-brand">
                Fin<span style="color:#4ADE80;">Sense</span>
            </div>
        </div>
        <div class="chat-header-status">
            <div class="status-dot"></div>
            Active
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Empty state
    if not st.session_state.messages:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">💬</div>
            <div class="empty-state-title">What's on your mind?</div>
            <div class="empty-state-sub">
                Ask me anything about your finances — 
                from building an emergency fund to calculating 
                your home loan EMI.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Suggestion chips
        suggestions = [
            "How much emergency fund do I need?",
            "Should I invest in SIP or FD?",
            "Calculate my home loan EMI",
            "I just got my first salary — what now?",
            "Help me plan my savings",
        ]

        cols = st.columns(3)
        for i, suggestion in enumerate(suggestions[:3]):
            with cols[i % 3]:
                if st.button(suggestion, key=f"suggestion_{i}",
                             use_container_width=True):
                    st.session_state.messages.append({
                        "role": "user",
                        "content": suggestion
                    })
                    with st.spinner(""):
                        try:
                            resp = requests.post(
                                f"{BACKEND_URL}/chat",
                                json={
                                    "user_id": user.id,
                                    "message": suggestion
                                },
                                timeout=30
                            )
                            reply = resp.json()["reply"]
                        except Exception as e:
                            reply = "Something went wrong. Please try again."

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": reply
                        })
                        st.session_state.profile = fetch_profile(user.id)
                        st.rerun()

        cols2 = st.columns(2)
        for i, suggestion in enumerate(suggestions[3:]):
            with cols2[i % 2]:
                if st.button(suggestion, key=f"suggestion_{i+3}",
                             use_container_width=True):
                    st.session_state.messages.append({
                        "role": "user",
                        "content": suggestion
                    })
                    with st.spinner(""):
                        try:
                            resp = requests.post(
                                f"{BACKEND_URL}/chat",
                                json={
                                    "user_id": user.id,
                                    "message": suggestion
                                },
                                timeout=30
                            )
                            reply = resp.json()["reply"]
                        except Exception as e:
                            reply = "Something went wrong. Please try again."

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": reply
                        })
                        st.session_state.profile = fetch_profile(user.id)
                        st.rerun()

    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about your finances..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(""):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/chat",
                        json={
                            "user_id": user.id,
                            "message": prompt
                        },
                        timeout=30
                    )
                    reply = response.json()["reply"]
                except Exception as e:
                    reply = "Something went wrong. Please try again in a moment."

            st.markdown(reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

        # Refresh profile after message
        st.session_state.profile = fetch_profile(user.id)

# ============ ROUTER ============

if st.session_state.user is None:
    show_auth_page()
else:
    show_chat_page()