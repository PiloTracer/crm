#!/bin/bash
export DEPLOY_ENV="PRD"
docker-compose -f docker-compose-PRD.yaml down
docker-compose -f docker-compose-PRD.yaml up --build -d --force-recreate