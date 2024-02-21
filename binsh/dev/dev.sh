#!/bin/bash
export DEPLOY_ENV="dev"
sudo docker-compose -f docker-compose-dev.yaml down
sudo docker-compose -f docker-compose-dev.yaml up --build -d --force-recreate