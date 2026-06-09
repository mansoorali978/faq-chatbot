# FAQ Chatbot

A simple FAQ chatbot with a FastAPI backend and React frontend, orchestrated with Docker Compose.

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