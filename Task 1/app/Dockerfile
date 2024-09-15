FROM python:3.12

WORKDIR /app

COPY . .

ENV FLASK_ENV=production

RUN pip install -r requirements.txt

EXPOSE 3000

CMD exec app python app.py