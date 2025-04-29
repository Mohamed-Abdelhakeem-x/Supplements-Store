FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=3000

EXPOSE 3000

CMD ["flask", "run", "--host=0.0.0.0"]