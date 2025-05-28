from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import requests

router = APIRouter()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_ID = os.getenv("GROQ_MODEL_ID")

class QueryRequest(BaseModel):
    query: str
    context: list[str] = []
    query_type: str  # e.g. "market_brief", "earnings_summary", ...

PROMPT_TEMPLATES = {
    "market_brief": """You are a financial assistant generating a concise morning market brief. Given the user's question and the financial context documents, synthesize a response that includes key portfolio risk exposure, earnings surprises, and regional market sentiment.

User Question:
{query}

Context:
{context}

Please provide a clear, structured, and informative market brief.
""",

    "earnings_summary": """You are a financial analyst specializing in earnings reports. Given the user query and relevant context, summarize the latest earnings results for the specified companies, highlighting beats, misses, revenue, and outlook.

User Question:
{query}

Context:
{context}

Provide a succinct earnings summary with key financial figures and notable commentary.
""",

    "stock_analysis": """You are a stock market expert providing detailed performance analysis. Based on the user question and financial data context, explain recent stock price movements, drivers, and outlook.

User Question:
{query}

Context:
{context}

Give a clear, data-backed performance analysis.
""",

    "risk_insight": """You are a risk management advisor. Given the user's question and supporting data, analyze current portfolio risks including sector exposures, volatility, and macroeconomic factors.

User Question:
{query}

Context:
{context}

Deliver a focused risk assessment with actionable insights.
""",

    "sentiment_news": """You are a financial news summarizer. Using the user query and news context, summarize the latest market sentiment, major news, and trends relevant to the user's portfolio or interests.

User Question:
{query}

Context:
{context}

Provide an engaging summary of market sentiment and key news events.
"""
}

@router.post("/answer")
def generate_answer(req: QueryRequest):
    template = PROMPT_TEMPLATES.get(req.query_type.lower())
    if not template:
        raise HTTPException(status_code=400, detail=f"Unknown query_type '{req.query_type}'. Valid types: {list(PROMPT_TEMPLATES.keys())}")

    prompt = template.format(
        query=req.query.strip(),
        context="\n".join(req.context)
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": GROQ_MODEL_ID,
        "prompt": prompt,
        "max_tokens": 384,
        "temperature": 0.3,
        "stop": ["\n\n"]
    }
    response = requests.post(
        "https://api.groq.ai/v1/generate",
        headers=headers,
        json=json_data
    )
    response.raise_for_status()
    result = response.json()
    generated_text = result.get("text", "").strip()
    return {"answer": generated_text}
