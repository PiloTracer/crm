#!/bin/bash
sudo docker-compose -f docker-compose-fastapi-PRD.yaml down
sudo docker-compose -f docker-compose-fastapi-PRD.yaml up --build -d --force-recreate