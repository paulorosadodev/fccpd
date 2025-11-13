FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY game_master.py .
RUN chmod +x game_master.py

ENV PYTHONUNBUFFERED=1

CMD ["python", "game_master.py"]
