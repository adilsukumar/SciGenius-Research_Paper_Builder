FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Spacy model during build
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Hugging Face Spaces run on port 7860 by default
ENV PORT=7860
EXPOSE 7860

# Start the FastAPI app
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "7860"]
