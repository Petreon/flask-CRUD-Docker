# flask-CRUD-Docker
First application using Flask, Postgre, docker and docker-compose

# clone the application

# create the postgre container
- $ docker compose up -d flask_db

# build the docker compose
- $ docker compose build

# Up the flask application
- $ docker compose up flask_app

# To rebuild an alteration
- $ docker compose up --build flask_app