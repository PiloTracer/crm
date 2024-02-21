#!/bin/bash
docker-compose -f docker-compose-api-dev.yaml down
docker-compose -f docker-compose-api-dev.yaml up --build -d --force-recreate