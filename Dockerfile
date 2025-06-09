FROM python:3.10-slim

RUN apt-get update && apt-get install -y libpq-dev && apt-get install curl -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV FLASK_APP=app

CMD ["flask", "run"]
