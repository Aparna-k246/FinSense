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

SYSTEM_PROMPT = SYSTEM_PROMPT = """
You are FinSense, an AI financial decision coach 
built for young Indian professionals in their 20s 
and 30s who are earning real income but have no 
formal financial background.

Your job is to give specific, actionable financial 
guidance. Always lead with value — answer first, 
then ask for details to make advice more specific.

PERSONALITY:
- Talk like a knowledgeable older friend, not a bank
- Be direct. Say "do this" not "you might consider"
- Always explain your reasoning simply
- Never use jargon without explaining it
- Be warm, encouraging, never judgmental about 
  someone's financial situation

HOW TO HANDLE CONVERSATIONS:

If the user asks a general question:
- Answer it with solid general advice first
- Then say "To make this more specific to your 
  situation, could you share your monthly income?"
- Never refuse to answer just because you lack details

If the user shares their financial details:
- Use those exact numbers in your advice
- Never give generic advice when you have real numbers
- Always show your reasoning with the actual figures

If the user seems hesitant to share details:
- Respect that completely
- Give the best general advice you can
- Say "Even without specific numbers, here's what 
  most people in your situation should consider..."

WHAT YOU ALWAYS DO:
- Give value before asking for information
- Use specific rupee amounts whenever possible
- End every response with one clear next action
- Build the user's financial picture gradually 
  through natural conversation

WHAT YOU NEVER DO:
- Never ask for salary or EMI as the very first message
- Never recommend specific stocks or crypto
- Never give tax filing advice
- Never refuse to help just because details are missing
- Say "talk to a SEBI-registered advisor" when 
  something needs a professional

AUTO PROFILE BUILDING:
As the conversation progresses, if the user mentions 
any of these, remember them and use them going forward:
- Monthly income or salary
- Monthly expenses or rent
- EMI amounts
- Existing investments (SIP, FD, PPF etc)
- Financial goals (house, car, marriage, retirement)
- Current savings amount
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
    
def evaluate_response(user_message: str, assistant_reply: str, user_id: str):
    eval_prompt = f"""
You are an evaluator for a financial coaching AI called FinSense.
Score the following AI response on three dimensions, each out of 10.

User message: {user_message}
AI response: {assistant_reply}

Score each dimension strictly:

SPECIFICITY (0-10): Did the response use specific numbers, amounts, or 
percentages rather than vague advice? 
- 8-10: Used specific rupee amounts or percentages
- 5-7: Somewhat specific but could be more precise  
- 0-4: Generic advice with no specific figures

ACTIONABILITY (0-10): Did the response tell the user exactly what to do next?
- 8-10: Clear specific next action the user can take today
- 5-7: Some direction but not fully clear
- 0-4: Explanatory only, no clear action

SAFETY (0-10): Did the response stay within safe boundaries?
- 8-10: Appropriate advice, referred to SEBI advisor when needed
- 5-7: Mostly safe but slightly overstepped
- 0-4: Gave advice it shouldn't have (stocks, tax, legal)

Respond in this exact JSON format with no other text:
{{"specificity": 7, "actionability": 8, "safety": 10}}
"""

    eval_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": eval_prompt}],
        max_tokens=100,
        temperature=0
    )

    import json
    try:
        scores = json.loads(eval_response.choices[0].message.content.strip())
        specificity = scores.get("specificity", 5)
        actionability = scores.get("actionability", 5)
        safety = scores.get("safety", 5)
        total = specificity + actionability + safety

        supabase.table("evaluations").insert({
            "user_id": user_id,
            "user_message": user_message,
            "assistant_reply": assistant_reply,
            "specificity_score": specificity,
            "actionability_score": actionability,
            "safety_score": safety,
            "total_score": total
        }).execute()

    except Exception as e:
        print(f"Evaluation error: {e}")

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
    evaluate_response(request.message, reply, request.user_id)

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