FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV AGENT_MANIFEST_FILE=/app/registries/manifest.hocon
ENV AGENT_TOOL_PATH=/app/coded_tools

EXPOSE 8000

# Start Neuro-SAN server + FastAPI together
CMD ["sh", "-c", "python -m neuro_san.service.main_loop.server_main_loop & uvicorn app.main:app --host 0.0.0.0 --port 8000"]