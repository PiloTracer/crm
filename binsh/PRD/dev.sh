#!/bin/bash
export DEPLOY_ENV="PRD"
sudo docker-compose -f docker-compose-PRD.yaml down
sudo docker-compose -f docker-compose-PRD.yaml up --build -d --force-recreate