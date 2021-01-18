FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/
RUN apt-get update
RUN apt-get install -y gcc python3-dev musl-dev postgresql-9.3
RUN pip install -r requirements.txt
COPY . /app/