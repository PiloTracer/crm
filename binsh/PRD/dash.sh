#!/bin/bash
docker-compose -f docker-compose-dashboard-PRD.yaml down
docker-compose -f docker-compose-dashboard-PRD.yaml build --no-cache
docker-compose -f docker-compose-dashboard-PRD.yaml up -d --force-recreate
