FROM python:3.12

WORKDIR /app

COPY . .

ENV FLASK_ENV=production

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=3000

CMD exec gunicorn --bind :$PORT app:app