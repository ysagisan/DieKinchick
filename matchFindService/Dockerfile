FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r /app/matchFindService/requirements.txt

CMD ["bash", "-c", "PYTHONPATH=/app python matchFindService/server_redis.py"]
