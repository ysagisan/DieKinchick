FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r /app/botSettings/requirements.txt

CMD ["bash", "-c", "PYTHONPATH=/app python botSettings/main.py"]

