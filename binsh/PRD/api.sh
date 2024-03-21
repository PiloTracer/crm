#!/bin/bash
sudo docker compose -f docker-compose-api-PRD.yaml down
sudo docker compose -f docker-compose-api-PRD.yaml up --build -d --force-recreate