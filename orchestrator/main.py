from fastapi import FastAPI
from agents.api_agent import router as api_router
from agents.scraping_agent import router as scraping_router
from retriever_agent.retriever import router as retriever_router
from agents.langchain_agent import router as langchain_router
from agents.voice_pipeline import router as voice_router
from voice.stt_tts import router as voice_router

app = FastAPI(title="Finance Voice Assistant with MCP")

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api")
app.include_router(scraping_router, prefix="/scrape")
app.include_router(retriever_router, prefix="/retriever")
app.include_router(langchain_router, prefix="/llm")
app.include_router(voice_router, prefix="/voice")

