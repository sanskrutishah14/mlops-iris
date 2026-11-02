FROM python:3.14-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=120 --retries 10 -r requirements.txt

COPY src/ ./src/
COPY streamlit_app.py .

# Train the model at build time so the image is self-contained
RUN python src/train.py

EXPOSE 8000 8501
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
