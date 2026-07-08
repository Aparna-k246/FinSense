from supabase import create_client
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from knowledge_base import FINANCIAL_KNOWLEDGE
import os
import json

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("Embedding knowledge base...")
for item in FINANCIAL_KNOWLEDGE:
    text = f"{item['title']}. {item['content']}"
    embedding = model.encode(text).tolist()
    
    supabase.table("financial_knowledge").insert({
        "title": item["title"],
        "content": item["content"],
        "category": item["category"],
        "embedding": embedding
    }).execute()
    
    print(f"Embedded: {item['title']}")

print("Done! Knowledge base ready.")