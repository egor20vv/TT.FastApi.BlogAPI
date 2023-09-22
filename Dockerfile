FROM python:3.11.1-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY ./app .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]