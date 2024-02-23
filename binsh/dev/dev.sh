#!/bin/bash
export DEPLOY_ENV="dev"

sudo docker compose -f docker-compose-pytap-dev.yaml down
sudo docker compose -f docker-compose-rabbitmq.yaml down
sudo docker compose -f docker-compose-fastapi-dev.yaml down
sudo docker compose -f docker-compose-dashboard-dev.yaml down
sudo docker compose -f docker-compose-api-dev.yaml down
sudo docker compose -f docker-compose-couchdb.yaml down

sudo docker compose -f docker-compose-pytap-dev.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-rabbitmq.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-fastapi-dev.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-dashboard-dev.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-api-dev.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-couchdb.yaml up --build -d --force-recreate
