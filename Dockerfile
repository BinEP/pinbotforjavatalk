FROM python:3.8-alpine

RUN mkdir /bot /bot-setup

COPY requirements.txt /bot-setup

RUN apk add gcc
RUN apk add musl-dev
RUN pip install -U -r /bot-setup/requirements.txt

COPY src/ /bot
WORKDIR /bot

CMD ["python", "pin-bot.py"]