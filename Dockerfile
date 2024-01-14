FROM python:3.10.12-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["flask","run","--debug","--host=0.0.0.0", "--port=4000", "--debug"]