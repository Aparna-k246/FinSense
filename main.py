from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

load_dotenv()

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# ============ FINANCIAL TOOLS ============

def calculate_sip_returns(monthly_amount: float, years: int, expected_rate: float) -> dict:
    monthly_rate = expected_rate / 100 / 12
    months = years * 12
    if monthly_rate == 0:
        future_value = monthly_amount * months
    else:
        future_value = monthly_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    total_invested = monthly_amount * months
    total_returns = future_value - total_invested
    return {
        "monthly_amount": monthly_amount,
        "years": years,
        "expected_rate": expected_rate,
        "total_invested": round(total_invested, 2),
        "future_value": round(future_value, 2),
        "total_returns": round(total_returns, 2)
    }

def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> dict:
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months / ((1 + monthly_rate) ** tenure_months - 1)
    total_payment = emi * tenure_months
    total_interest = total_payment - principal
    return {
        "principal": principal,
        "annual_rate": annual_rate,
        "tenure_months": tenure_months,
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2)
    }

def check_emergency_fund(monthly_expenses: float, current_savings: float) -> dict:
    minimum_required = monthly_expenses * 3
    recommended = monthly_expenses * 6
    shortfall = max(0, recommended - current_savings)
    status = "adequate" if current_savings >= recommended else "insufficient"
    months_to_build = shortfall / (monthly_expenses * 0.2) if shortfall > 0 else 0
    return {
        "monthly_expenses": monthly_expenses,
        "current_savings": current_savings,
        "minimum_required": minimum_required,
        "recommended": recommended,
        "shortfall": round(shortfall, 2),
        "status": status,
        "months_to_build_at_20_percent_savings": round(months_to_build, 1)
    }

def calculate_fd_returns(principal: float, annual_rate: float, years: int) -> dict:
    quarters = years * 4
    quarterly_rate = annual_rate / 100 / 4
    maturity_amount = principal * (1 + quarterly_rate) ** quarters
    total_interest = maturity_amount - principal
    return {
        "principal": principal,
        "annual_rate": annual_rate,
        "years": years,
        "maturity_amount": round(maturity_amount, 2),
        "total_interest": round(total_interest, 2)
    }

def execute_tool(tool_name: str, tool_args: dict) -> dict:
    if tool_name == "calculate_sip_returns":
        return calculate_sip_returns(**tool_args)
    elif tool_name == "calculate_emi":
        return calculate_emi(**tool_args)
    elif tool_name == "check_emergency_fund":
        return check_emergency_fund(**tool_args)
    elif tool_name == "calculate_fd_returns":
        return calculate_fd_returns(**tool_args)
    else:
        return {"error": f"Unknown tool: {tool_name}"}

# ============ TOOL DEFINITIONS FOR GEMINI ============

TOOLS = [
    genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="calculate_sip_returns",
                description="Calculate the future value of a monthly SIP investment. Use when user asks about SIP returns, investment growth, or corpus from regular investing.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "monthly_amount": genai.protos.Schema(
                            type=genai.protos.Type.NUMBER,
                            description="Monthly SIP amount in full rupees. 1 lakh = 100000, 50000 rupees = 50000"
                        ),
                        "years": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Investment duration in years"
                        ),
                        "expected_rate": genai.protos.Schema(
                            type=genai.protos.Type.NUMBER,
                            description="Expected annual return rate as percentage. Use 12 as default for equity mutual funds"
                        )
                    },
                    required=["monthly_amount", "years", "expected_rate"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="calculate_emi",
                description="Calculate EMI for any loan - home loan, car loan, personal loan. Use when user asks about loan EMI or affordability.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "principal": genai.protos.Schema(
                            type=genai.protos.Type.NUMBER,
                            description="Loan amount in full rupees. Convert: 50 lakhs = 5000000, 1 crore = 10000000"
                        ),
                        "annual_rate": genai.protos.Schema(
                            type=genai.protos.Type.NUMBER,
                            description="Annual interest rate as percentage"
                        ),
                        "tenure_months": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Loan tenure in months. Convert years to months: 20 years = 240 months"
                        )
                    },
                    required=["principal", "annual_rate", "tenure_months"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="check_emergency_fund",
                description="Check if user has adequate emergency fund. Use before giving investment advice when user mentions expenses and savings.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "monthly_expenses": genai.protos.Schema(
                            type=genai.protos.Type.NUMBER,
                            description="Total monthly expenses in full rupees"
                        ),
                        "current_savings": genai.protos.Schema(
                            type=genai.protos.Type.NUMBER,
                            description="Current savings in full rupees"
                        )
                    },
                    required=["monthly_expenses", "current_savings"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="calculate_fd_returns",
                description="Calculate Fixed Deposit maturity amount. Use when user asks about FD returns or wants to compare FD vs SIP.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "principal": genai.protos.Schema(
                            type=genai.protos.Type.NUMBER,
                            description="FD amount in full rupees. Convert: 50 lakhs = 5000000, 1 crore = 10000000"
                        ),
                        "annual_rate": genai.protos.Schema(
                            type=genai.protos.Type.NUMBER,
                            description="Annual interest rate as percentage. Use 7 as default for major banks"
                        ),
                        "years": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="FD duration in years"
                        )
                    },
                    required=["principal", "annual_rate", "years"]
                )
            )
        ]
    )
]

# ============ SYSTEM PROMPT ============

SYSTEM_PROMPT = """
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

TOOL USAGE:
You have financial calculator tools. ALWAYS use them:
- calculate_emi: for ANY loan or EMI question
- calculate_sip_returns: for ANY SIP or investment growth question
- calculate_fd_returns: for ANY fixed deposit question
- check_emergency_fund: when user mentions savings and expenses
Never estimate calculations manually. Always call the tool.
"""

# ============ DATABASE FUNCTIONS ============

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

SPECIFICITY (0-10): Did the response use specific numbers, amounts, or percentages?
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
- 0-4: Gave advice it shouldn't have

Respond in this exact JSON format with no other text:
{{"specificity": 7, "actionability": 8, "safety": 10}}
"""
    try:
        eval_model = genai.GenerativeModel("gemini-1.5-flash")
        eval_response = eval_model.generate_content(eval_prompt)
        scores = json.loads(eval_response.text.strip())
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

# ============ ROUTES ============

@app.get("/")
def root():
    return {"message": "FinSense is running"}

@app.get("/test-tool")
def test_tool():
    result = calculate_emi(5000000, 8.5, 240)
    return result

@app.post("/chat")
def chat(request: ChatRequest):
    profile = get_user_profile(request.user_id)
    history = get_conversation_history(request.user_id)

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

Use this context to give specific personalised advice.
Do not ask for information you already have.
"""

    # Build Gemini chat history
    gemini_history = []
    for turn in history:
        role = "user" if turn["role"] == "user" else "model"
        gemini_history.append({
            "role": role,
            "parts": [turn["content"]]
        })

    # Create Gemini model with system instruction
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT + profile_context,
        tools=TOOLS
    )

    # Start chat with history
    chat_session = model.start_chat(history=gemini_history)

    # Send message
    response = chat_session.send_message(request.message)

    # Handle tool calls
    reply = ""
    while True:
        # Check if Gemini wants to call a tool
        tool_call_found = False
        for part in response.parts:
            if hasattr(part, 'function_call') and part.function_call.name:
                tool_call_found = True
                tool_name = part.function_call.name
                tool_args = dict(part.function_call.args)

                print(f"Tool called: {tool_name} with args: {tool_args}")

                tool_result = execute_tool(tool_name, tool_args)

                print(f"Tool result: {tool_result}")

                # Send tool result back to Gemini
                response = chat_session.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=tool_name,
                                response={"result": tool_result}
                            )
                        )]
                    )
                )
                break

        if not tool_call_found:
            # Extract text response
            reply = response.text
            break

    save_message(request.user_id, "user", request.message)
    save_message(request.user_id, "assistant", reply)
    evaluate_response(request.message, reply, request.user_id)

    return {
        "reply": reply,
        "user_id": request.user_id
    }

@app.post("/update-profile")
def update_profile(user_id: str, updates: dict):
    from pydantic import BaseModel as PydanticBaseModel
    return {"message": "Profile updated successfully"}

@app.get("/profile/{user_id}")
def get_profile(user_id: str):
    profile = get_user_profile(user_id)
    if profile:
        return profile
    return {"message": "No profile found"}