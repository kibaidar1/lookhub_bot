FROM python:3.11-alpine

WORKDIR /bot

COPY ./requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./telegram_bot.py" ]