FROM python:3.11-slim

LABEL maintainer="Sahil Singh <sahilsingh8300@gmail.com>"
LABEL description="Sentiment Analysis Chatbot"
LABEL version="1.1.0"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import nltk; nltk.download('vader_lexicon', quiet=True)"

COPY . .

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["python", "main.py"]
