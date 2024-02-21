#!/bin/bash
sudo docker-compose -f docker-compose-dashboard-PRD.yaml down
sudo docker-compose -f docker-compose-dashboard-PRD.yaml build --no-cache
sudo docker-compose -f docker-compose-dashboard-PRD.yaml up -d --force-recreate
