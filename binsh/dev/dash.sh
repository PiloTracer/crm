#!/bin/bash
sudo docker compose -f docker-compose-dashboard-dev.yaml down
sudo docker compose -f docker-compose-dashboard-dev.yaml build --no-cache
sudo docker compose -f docker-compose-dashboard-dev.yaml up -d --force-recreate
