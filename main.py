from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

SYSTEM_PROMPT = """
You are FinSense, an AI financial decision coach 
built for young Indian professionals in their 20s 
and 30s who are earning real income but have no 
formal financial background.

Your job is to think through their specific 
financial situation and tell them clearly what 
to do next and why.

PERSONALITY:
- Talk like a knowledgeable older friend, not a bank
- Be direct. Say "do this" not "you might consider"
- Always explain your reasoning simply
- Never use jargon without explaining it

WHEN A USER ARRIVES:
- Ask ONE question at a time to build their picture
- Start by asking their monthly income and biggest 
  financial worry

WHAT YOU NEVER DO:
- Never recommend specific stocks or crypto
- Never give tax advice
- Say "talk to a SEBI-registered advisor" when 
  something needs a professional
"""

class ChatRequest(BaseModel):
    user_id: str
    message: str

def get_user_profile(user_id: str):
    result = supabase.table("user_profiles")\
        .select("*")\
        .eq("user_id", user_id)\
        .execute()
    if result.data:
        return result.data[0]
    return None

def save_user_profile(user_id: str, updates: dict):
    existing = get_user_profile(user_id)
    if existing:
        supabase.table("user_profiles")\
            .update(updates)\
            .eq("user_id", user_id)\
            .execute()
    else:
        supabase.table("user_profiles")\
            .insert({"user_id": user_id, **updates})\
            .execute()

def get_conversation_history(user_id: str, limit: int = 10):
    result = supabase.table("conversation_history")\
        .select("role, content")\
        .eq("user_id", user_id)\
        .order("created_at")\
        .limit(limit)\
        .execute()
    return result.data if result.data else []

def save_message(user_id: str, role: str, content: str):
    supabase.table("conversation_history")\
        .insert({
            "user_id": user_id,
            "role": role,
            "content": content
        })\
        .execute()

@app.get("/")
def root():
    return {"message": "FinSense is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    # Get user profile and history from Supabase
    profile = get_user_profile(request.user_id)
    history = get_conversation_history(request.user_id)

    # Build context from profile
    profile_context = ""
    if profile:
        profile_context = f"""
Known information about this user:
- Monthly income: {profile.get('monthly_income', 'not provided')}
- Fixed expenses: {profile.get('fixed_expenses', 'not provided')}
- EMI amount: {profile.get('emi_amount', 'not provided')}
- Existing investments: {profile.get('existing_investments', 'not provided')}
- Financial goals: {profile.get('financial_goals', 'not provided')}
- Biggest worry: {profile.get('biggest_worry', 'not provided')}

Use this context to give specific, personalised advice.
Do not ask for information you already have.
"""

    # Build messages
    messages = [{
        "role": "system",
        "content": SYSTEM_PROMPT + profile_context
    }]

    for turn in history:
        messages.append({
            "role": turn["role"],
            "content": turn["content"]
        })

    messages.append({
        "role": "user",
        "content": request.message
    })

    # Call Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    reply = response.choices[0].message.content

    # Save to Supabase
    save_message(request.user_id, "user", request.message)
    save_message(request.user_id, "assistant", reply)

    return {
        "reply": reply,
        "user_id": request.user_id
    }

@app.post("/update-profile")
def update_profile(user_id: str, updates: dict):
    save_user_profile(user_id, updates)
    return {"message": "Profile updated successfully"}

@app.get("/profile/{user_id}")
def get_profile(user_id: str):
    profile = get_user_profile(user_id)
    if profile:
        return profile
    return {"message": "No profile found"}