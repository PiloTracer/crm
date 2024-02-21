#!/bin/bash
sudo docker-compose -f docker-compose-fastapi-dev.yaml down
sudo docker-compose -f docker-compose-fastapi-dev.yaml up --build -d --force-recreate