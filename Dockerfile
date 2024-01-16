FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV MONGO_HOST="mongodb://localhost"
ENV MONGO_PORT="27017"

COPY . .

CMD ["python3", "-m", "main", "--host=0.0.0.0"]