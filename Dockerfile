FROM python:slim

WORKDIR /app
COPY requirements.lock ./
RUN pip install -U pip
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY src .
CMD python main.py
