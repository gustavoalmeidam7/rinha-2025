FROM python:3.12-slim

WORKDIR /app

COPY requiriments.txt .

RUN pip install --no-cache-dir -r requiriments.txt

COPY . .

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9999"]
