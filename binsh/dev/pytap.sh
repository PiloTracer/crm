#!/bin/bash
sudo docker compose -f docker-compose-pytap-dev.yaml down
sudo docker compose -f docker-compose-pytap-dev.yaml up --build -d --force-recreate