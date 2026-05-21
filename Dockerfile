FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY server.py .
COPY README.md report.md ai_usage.md ./
COPY evaluation ./evaluation
COPY results ./results

CMD ["python", "server.py"]
