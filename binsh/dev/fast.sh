#!/bin/bash
docker-compose -f docker-compose-fastapi-dev.yaml down
docker-compose -f docker-compose-fastapi-dev.yaml up --build -d --force-recreate