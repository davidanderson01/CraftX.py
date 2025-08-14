# Stage 1: Ollama base to build model - pinned to a specific secure version
FROM ollama/ollama:0.1.29 AS ollama_base
COPY Modelfile /root/Modelfile
RUN ollama serve & \
    sleep 4 && \
    ollama pull llama3.2 && \
    ollama create davidanderson01/craftx -f /root/Modelfile

# Stage 2: API container - using Debian slim-based Python for better security
FROM python:3.13-slim

# Install security updates and curl for healthcheck
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl bash && \
    apt-get autoremove -y && \
    apt-get clean && \
# Create non-root user for security
RUN groupadd -r craftx && useradd -r -g craftx craftx
# Create non-root user for security
RUN groupadd -r craftx && useradd -r -g craftx craftx
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY craftx.py .
COPY start.sh .
RUN chmod +x start.sh
COPY --from=ollama_base /bin/ollama /bin/ollama
COPY --from=ollama_base /root/.ollama /root/.ollama

# Change ownership of ollama data to craftx user
RUN chown -R craftx:craftx /root/.ollama && chown craftx:craftx start.sh

ENV OLLAMA_HOST=0.0.0.0
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Switch to non-root user for the application
USER craftx

# Use JSON format for proper signal handling
CMD ["/bin/bash", "./start.sh"]
