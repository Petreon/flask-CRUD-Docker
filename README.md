# Flask-CRUD-Docker
First CRUD application using Flask, Postgre, docker and docker-compose,
the application was been tested with postman for the routes and with tableplus
for the postgre database

## Clone the application
- $ git clone https://github.com/Petreon/flask-CRUD-Docker.git

## Create the postgre container
- $ docker compose up -d flask_db

## Build the docker compose
- $ docker compose build

## Up the flask application
- $ docker compose up flask_app

## To rebuild an alteration
- $ docker compose up --build flask_app