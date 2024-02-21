#!/bin/bash
export DEPLOY_ENV="dev"
docker-compose -f docker-compose-dev.yaml down
docker-compose -f docker-compose-dev.yaml up --build -d --force-recreate