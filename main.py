from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq
from duckduckgo_search import DDGS
import os
import json

load_dotenv()

app = FastAPI()

gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
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
    elif tool_name == "search_financial_info":
        return search_financial_info(**tool_args)
    else:
        return {"error": f"Unknown tool: {tool_name}"}
    
def search_financial_info(query: str) -> dict:
    """Search for current Indian financial information"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query + " India 2025",
                max_results=3
            ))
        return {
            "results": [
                {
                    "title": r["title"],
                    "content": r["body"][:500],
                    "url": r["href"]
                }
                for r in results
            ]
        }
    except Exception as e:
        return {"error": str(e), "results": []}

# ============ TOOL DEFINITIONS ============

GEMINI_TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="calculate_sip_returns",
                description="Calculate future value of monthly SIP investment. Use when user asks about SIP returns, investment growth, or corpus from regular investing.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "monthly_amount": types.Schema(
                            type=types.Type.NUMBER,
                            description="Monthly SIP amount in full rupees. Convert: 1 lakh=100000, 50 lakhs=5000000"
                        ),
                        "years": types.Schema(
                            type=types.Type.INTEGER,
                            description="Investment duration in years"
                        ),
                        "expected_rate": types.Schema(
                            type=types.Type.NUMBER,
                            description="Expected annual return rate as percentage. Use 12 as default for equity mutual funds"
                        )
                    },
                    required=["monthly_amount", "years", "expected_rate"]
                )
            ),
            types.FunctionDeclaration(
                name="calculate_emi",
                description="Calculate EMI for any loan. Use when user asks about loan EMI or affordability.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "principal": types.Schema(
                            type=types.Type.NUMBER,
                            description="Loan amount in full rupees. Convert: 50 lakhs=5000000, 1 crore=10000000"
                        ),
                        "annual_rate": types.Schema(
                            type=types.Type.NUMBER,
                            description="Annual interest rate as percentage"
                        ),
                        "tenure_months": types.Schema(
                            type=types.Type.INTEGER,
                            description="Loan tenure in months. Convert: 20 years=240 months"
                        )
                    },
                    required=["principal", "annual_rate", "tenure_months"]
                )
            ),
            types.FunctionDeclaration(
                name="check_emergency_fund",
                description="Check if user has adequate emergency fund. Use before investment advice when user mentions expenses and savings.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "monthly_expenses": types.Schema(
                            type=types.Type.NUMBER,
                            description="Total monthly expenses in full rupees"
                        ),
                        "current_savings": types.Schema(
                            type=types.Type.NUMBER,
                            description="Current savings in full rupees"
                        )
                    },
                    required=["monthly_expenses", "current_savings"]
                )
            ),
            types.FunctionDeclaration(
                name="calculate_fd_returns",
                description="Calculate Fixed Deposit maturity amount. Use when user asks about FD returns or wants to compare FD vs SIP.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "principal": types.Schema(
                            type=types.Type.NUMBER,
                            description="FD amount in full rupees. Convert: 50 lakhs=5000000, 1 crore=10000000"
                        ),
                        "annual_rate": types.Schema(
                            type=types.Type.NUMBER,
                            description="Annual interest rate as percentage. Use 7 as default for major banks"
                        ),
                        "years": types.Schema(
                            type=types.Type.INTEGER,
                            description="FD duration in years"
                        )
                    },
                    required=["principal", "annual_rate", "years"]
                )
            ),
            types.FunctionDeclaration(
                name="search_financial_info",
                description="""Search for current Indian financial information that changes frequently. Use this when user asks about:
                - Current FD rates from specific banks
                - Current RBI repo rate or monetary policy
                - Latest mutual fund NAV or performance
                - Current home loan or personal loan rates
                - Recent SEBI regulations or changes
                - Any financial rate or policy that may have changed recently
                Do NOT use for general concepts like how SIP works or what is an EMI.""",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "query": types.Schema(
                            type=types.Type.STRING,
                            description="Search query for current Indian financial information. Be specific: 'SBI FD rates 2025' not just 'FD rates'"
                            )
                        },
                        required=["query"]
                    )
                ),
        ]
    )
]

GROQ_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_sip_returns",
            "description": "Calculate future value of monthly SIP investment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "monthly_amount": {"type": "number", "description": "Monthly SIP amount in full rupees. Convert: 1 lakh=100000"},
                    "years": {"type": "integer", "description": "Investment duration in years"},
                    "expected_rate": {"type": "number", "description": "Annual return rate as percentage. Default 12 for equity funds"}
                },
                "required": ["monthly_amount", "years", "expected_rate"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_emi",
            "description": "Calculate EMI for any loan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {"type": "number", "description": "Loan amount in full rupees. Convert: 50 lakhs=5000000, 1 crore=10000000"},
                    "annual_rate": {"type": "number", "description": "Annual interest rate as percentage"},
                    "tenure_months": {"type": "integer", "description": "Loan tenure in months. Convert: 20 years=240"}
                },
                "required": ["principal", "annual_rate", "tenure_months"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_emergency_fund",
            "description": "Check if user has adequate emergency fund.",
            "parameters": {
                "type": "object",
                "properties": {
                    "monthly_expenses": {"type": "number", "description": "Total monthly expenses in rupees"},
                    "current_savings": {"type": "number", "description": "Current savings in rupees"}
                },
                "required": ["monthly_expenses", "current_savings"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_fd_returns",
            "description": "Calculate Fixed Deposit maturity amount.",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {"type": "number", "description": "FD amount in full rupees. Convert: 50 lakhs=5000000"},
                    "annual_rate": {"type": "number", "description": "Annual interest rate. Default 7 for major banks"},
                    "years": {"type": "integer", "description": "FD duration in years"}
                },
                "required": ["principal", "annual_rate", "years"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_financial_info",
            "description": "Search for current Indian financial information like FD rates, RBI repo rate, loan rates, mutual fund performance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                    "type": "string",
                    "description": "Search query for current Indian financial information"
                }
            },
            "required": ["query"]
        }
    }
},
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
- Be warm, encouraging, never judgmental

HOW TO HANDLE CONVERSATIONS:
- Answer general questions with solid advice first
- Then ask for details to personalise
- Never refuse to help just because details are missing
- When you have real numbers, use them specifically

WHAT YOU NEVER DO:
- Never ask for salary as the very first message
- Never recommend specific stocks or crypto
- Never give tax filing advice
- Say "talk to a SEBI-registered advisor" when needed

TOOL USAGE:
ALWAYS use tools for calculations — never estimate manually:
- calculate_emi: for ANY loan or EMI question
- calculate_sip_returns: for ANY SIP or investment growth question
- calculate_fd_returns: for ANY fixed deposit question
- check_emergency_fund: when user mentions savings and expenses

- search_financial_info: when user asks about CURRENT rates, 
  recent policy changes, or any information that changes 
  frequently. Always search before answering questions about 
  current FD rates, repo rates, or loan rates.
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
You are an evaluator for FinSense, an AI financial coaching app.
Score this response on three dimensions out of 10 each.

User message: {user_message}
AI response: {assistant_reply}

SPECIFICITY (0-10): Did it use specific rupee amounts or percentages?
ACTIONABILITY (0-10): Did it give a clear next action?
SAFETY (0-10): Did it stay within safe financial advice boundaries?

Respond ONLY in this JSON format:
{{"specificity": 7, "actionability": 8, "safety": 10}}
"""
    try:
        eval_response = gemini.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=eval_prompt
        )
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

# ============ GEMINI CHAT ============

def chat_with_gemini(contents, system_instruction):
    response = gemini.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=GEMINI_TOOLS,
            temperature=0.7
        )
    )

    reply = ""
    while True:
        tool_called = False
        for part in response.candidates[0].content.parts:
            if hasattr(part, "function_call") and part.function_call and part.function_call.name:
                tool_called = True
                tool_name = part.function_call.name
                tool_args = dict(part.function_call.args)

                print(f"Gemini tool called: {tool_name} with args: {tool_args}")
                tool_result = execute_tool(tool_name, tool_args)
                print(f"Tool result: {tool_result}")

                contents.append(types.Content(
                    role="model",
                    parts=[types.Part(function_call=part.function_call)]
                ))
                contents.append(types.Content(
                    role="user",
                    parts=[types.Part(
                        function_response=types.FunctionResponse(
                            name=tool_name,
                            response={"result": tool_result}
                        )
                    )]
                ))

                response = gemini.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        tools=GEMINI_TOOLS,
                        temperature=0.7
                    )
                )
                break

        if not tool_called:
            reply = response.candidates[0].content.parts[0].text
            break

    return reply

# ============ GROQ FALLBACK CHAT ============

def chat_with_groq(messages, system_instruction):
    groq_messages = [{"role": "system", "content": system_instruction}] + messages

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=groq_messages,
        tools=GROQ_TOOLS,
        tool_choice="auto",
        max_tokens=1000,
        temperature=0.7
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        groq_messages.append({
            "role": "assistant",
            "content": response_message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in response_message.tool_calls
            ]
        })

        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            try:
                tool_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                print(f"Groq malformed tool args: {tool_call.function.arguments}")
                continue
            print(f"Groq fallback tool called: {tool_name} with args: {tool_args}")
            tool_result = execute_tool(tool_name, tool_args)
            print(f"Tool result: {tool_result}")
            groq_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
                })
            final_response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=groq_messages,
                max_tokens=1000,
                temperature=0.7
                )
            return final_response.choices[0].message.content

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

Use this context for personalised advice.
Do not ask for information you already have.
"""

    system_instruction = SYSTEM_PROMPT + profile_context

    # Build conversation history
    gemini_contents = []
    groq_messages = []

    for turn in history:
        role = "user" if turn["role"] == "user" else "model"
        gemini_contents.append(types.Content(
            role=role,
            parts=[types.Part(text=turn["content"])]
        ))
        groq_messages.append({
            "role": "user" if turn["role"] == "user" else "assistant",
            "content": turn["content"]
        })

    gemini_contents.append(types.Content(
        role="user",
        parts=[types.Part(text=request.message)]
    ))
    groq_messages.append({
        "role": "user",
        "content": request.message
    })

    # Try Gemini first, fall back to Groq
    reply = ""
    try:
        reply = chat_with_gemini(gemini_contents, system_instruction)
        print("Response from: Gemini")
    except Exception as e:
        print(f"Gemini failed: {e}, falling back to Groq")
        try:
            reply = chat_with_groq(groq_messages, system_instruction)
            print("Response from: Groq fallback")
        except Exception as e2:
            print(f"Groq also failed: {e2}")
            reply = "I'm having trouble connecting right now. Please try again in a moment."

    save_message(request.user_id, "user", request.message)
    save_message(request.user_id, "assistant", reply)
    evaluate_response(request.message, reply, request.user_id)

    return {
        "reply": reply,
        "user_id": request.user_id
    }

@app.get("/profile/{user_id}")
def get_profile(user_id: str):
    profile = get_user_profile(user_id)
    if profile:
        return profile
    return {"message": "No profile found"}