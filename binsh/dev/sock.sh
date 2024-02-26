#!/bin/bash
sudo docker compose -f docker-compose-sock-dev.yaml down
sudo docker compose -f docker-compose-sock-dev.yaml up --build -d --force-recreate