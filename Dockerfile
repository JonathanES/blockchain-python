FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Disable Python output buffering
ENV PYTHONUNBUFFERED=1

# Copy application code
COPY blockchain.py .

# Run the script
CMD ["python", "blockchain.py"]
