#!/bin/sh

# Start Ollama in the background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
while ! ollama list >/dev/null 2>&1; do
    sleep 2
done
echo "Ollama is ready!"

# Start FastAPI
echo "Starting FastAPI server..."
exec uvicorn craftx:app --host 0.0.0.0 --port 8000
