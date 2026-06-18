# FinSense - AI Financial Decision Coach

An AI-powered financial coaching agent for young professionals 
who earn real income but have no formal financial background.

## What it does
FinSense acts as a knowledgeable older friend for financial decisions.
It asks the right questions, understands your specific situation and 
tells you clearly what to do next and why.

## Features
- Personalised financial advice based on your actual numbers
- Persistent memory across sessions, never repeats the same questions
- Built-in evaluation layer scoring every response on specificity, 
  actionability and safety
- Knows when to refer to a SEBI-registered advisor

## Tech Stack
- FastAPI : backend API
- Groq LLM (Llama 3.3 70B) : AI brain
- Supabase : persistent memory and evaluation logging
- Streamlit : chat interface

## Architecture
User message → FastAPI → Supabase fetches user profile (RAG) → 
Groq LLM generates response → Evaluation rubric scores response → 
Logged to Supabase → User sees advice

## Running locally
1. Clone the repo
2. Create .env from .env.example and add your keys
3. Install dependencies: pip install -r requirements.txt
4. Start backend: uvicorn main:app --reload
5. Start frontend: streamlit run app.py

## Built by
Aparna K - Applied AI Engineer
github.com/Aparna-k246
linkedin.com/in/aparna-k-628005167