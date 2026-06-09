from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router

app = FastAPI(
    title="FAQ Chatbot API",
    description="REST API for ICICI Pru Life FAQ Chatbot powered by Neuro-SAN",
    version="1.0.0"
)

# Allow frontend (React) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict in production
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}