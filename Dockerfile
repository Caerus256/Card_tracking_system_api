FROM python:3.11.7

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache -r requirements.txt

COPY . .

CMD [ "python3","-m","flask","run","--host=0.0.0.0"]
