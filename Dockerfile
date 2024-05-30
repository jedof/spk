FROM python:3.11-slim-bullseye

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ADD ./main.py .
ADD ./hendlers.py .
ADD ./.env .
