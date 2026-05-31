FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot/
COPY db/ ./db/
COPY web/ ./web/

COPY main.py .

RUN mkdir logs

CMD ["python", "main.py"]
