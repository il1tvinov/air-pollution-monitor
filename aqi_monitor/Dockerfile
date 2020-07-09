FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
# install psycopg2 dependencies
RUN apt-get update
RUN apt-get install -y gcc python3-dev musl-dev postgresql-9.3

ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/