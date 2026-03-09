FROM python:3.12-slim-bullseye

# Install system dependencies for audio processing (libsndfile for librosa) and psycopg2
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    gcc \
    libpq-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]