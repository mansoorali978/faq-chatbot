# FAQ Chatbot — Neuro-SAN powered

A full-stack FAQ chatbot for ICICI Pru Life built with React, FastAPI, and Neuro-SAN.

## Architecture

User → React Frontend → FastAPI Backend → Neuro-SAN Agent Server
↓
FaqLookupTool (CodedTool)
↓
FAQ JSON Dataset

## How Neuro-SAN Works

Neuro-SAN is a data-driven multi-agent framework where agent networks are defined
in HOCON config files. Our network has two agents:

1. **faq_frontman** — The front-facing LLM agent. Receives user questions,
   maintains conversation context (multi-turn), and delegates data lookups to
   the FaqLookupTool.

2. **FaqLookupTool** — A CodedTool (Python class) that searches the FAQ JSON
   dataset using keyword matching and returns relevant Q&A pairs to the frontman.

The AAOSA protocol lets agents autonomously decide when to delegate, enabling
natural multi-turn conversations like:
> User: "How do I change my bank account?"
> Bot: "You can change it by submitting..."
> User: "Is there any charge?"
> Bot: "No, there is no charge." ← context maintained from previous turn

## Prerequisites

- Docker & Docker Compose
- OpenAI API key (or Anthropic / Ollama)

## Quick Start

```bash
git clone https://github.com/mansoorali978/faq-chatbot.git
cd faq-chatbot
cp .env.example .env       # Add your OPENAI_API_KEY
docker compose up --build
```

Visit **http://localhost:3000**

## DockerHub Images

- Backend: `docker pull mansoorali978/faq-chatbot-backend:latest`
- Frontend: `docker pull mansoorali978/faq-chatbot-frontend:latest`

## API Reference

### POST /api/v1/chat

Request:
```json
{
  "message": "How do I change my bank account?",
  "session_id": "abc123",
  "chat_context": null
}
```

Response:
```json
{
  "answer": "You can change your registered bank account by...",
  "session_id": "abc123",
  "chat_context": { ... }
}
```

## Project Structure

```
faq-chatbot/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── main.py        # FastAPI entry point
│   │   ├── routes/
│   │   │   └── chat.py    # POST /chat endpoint
│   │   └── services/
│   │       └── neuro_san_client.py  # Neuro-SAN HTTP client
│   ├── registries/
│   │   ├── manifest.hocon           # Neuro-SAN agent manifest
│   │   └── faq_agent.hocon          # Agent network definition
│   ├── coded_tools/
│   │   └── faq_agent/
│   │       └── faq_lookup_tool.py   # CodedTool: searches FAQ data
│   ├── data/
│   │   └── faq.json                 # Static FAQ dataset
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   └── InputBar.jsx
│   │   └── api/
│   │       └── chat.js    # API call to backend
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── README.md
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Run with Docker Compose

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

### Run Locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## API

### POST /api/chat

Request:
```json
{ "message": "How do I reset my password?" }
```

Response:
```json
{ "reply": "Go to Settings > Security > Reset Password and follow the instructions." }