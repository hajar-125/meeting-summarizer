FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY src/app.py .

RUN mkdir -p uploads outputs

# Script de démarrage
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8000 8501

CMD ["./start.sh"]