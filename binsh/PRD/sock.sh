#!/bin/bash
sudo docker compose -f docker-compose-sock-PRD.yaml down
sudo docker compose -f docker-compose-sock-PRD.yaml up --build -d --force-recreate