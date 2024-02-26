#!/bin/bash
export DEPLOY_ENV="PRD"

sudo docker compose -f docker-compose-pytap-PRD.yaml down
sudo docker compose -f docker-compose-sock-PRD.yaml down
sudo docker compose -f docker-compose-rabbitmq.yaml down
sudo docker compose -f docker-compose-fastapi-PRD.yaml down
sudo docker compose -f docker-compose-dashboard-PRD.yaml down
sudo docker compose -f docker-compose-api-PRD.yaml down
sudo docker compose -f docker-compose-couchdb.yaml down
sudo docker compose -f docker-compose-redis.yaml down

sudo docker compose -f docker-compose-pytap-PRD.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-sock-PRD.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-rabbitmq.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-fastapi-PRD.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-dashboard-PRD.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-api-PRD.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-couchdb.yaml up --build -d --force-recreate
sudo docker compose -f docker-compose-redis.yaml up --build -d --force-recreate
