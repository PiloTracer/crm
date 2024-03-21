#!/bin/bash
sudo docker compose -f docker-compose-pytap-PRD.yaml down
sudo docker compose -f docker-compose-pytap-PRD.yaml up --build -d --force-recreate