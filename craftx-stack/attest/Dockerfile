FROM python:3.12-slim

# Apply security updates
RUN apk update && apk upgrade && apk add --no-cache curl ca-certificates && \
    rm -rf /var/cache/apk/*

# Create non-root user for security
RUN adduser -D -s /bin/sh craftx

WORKDIR /app
COPY anchor_proof.py .
RUN pip install --no-cache-dir web3 eth-account requests

# Switch to non-root user
USER craftx

CMD ["sh", "-c", "while true; do python anchor_proof.py; sleep 86400; done"]
