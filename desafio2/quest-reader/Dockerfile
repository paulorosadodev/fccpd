FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quest_reader.py .
RUN chmod +x quest_reader.py

ENV PYTHONUNBUFFERED=1

CMD ["python", "quest_reader.py"]
