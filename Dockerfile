
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
COPY backend /app/backend
COPY frontend /app/frontend

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app.wsgi:app"] 