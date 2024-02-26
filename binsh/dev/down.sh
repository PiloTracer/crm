#!/bin/bash
sudo docker compose -f docker-compose-pytap-dev.yaml down
sudo docker compose -f docker-compose-sock-dev.yaml down
sudo docker compose -f docker-compose-rabbitmq.yaml down
sudo docker compose -f docker-compose-fastapi-dev.yaml down
sudo docker compose -f docker-compose-dashboard-dev.yaml down
sudo docker compose -f docker-compose-api-dev.yaml down
sudo docker compose -f docker-compose-couchdb.yaml down
sudo docker compose -f docker-compose-redis.yaml down
