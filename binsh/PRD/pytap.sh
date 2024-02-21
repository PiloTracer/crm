#!/bin/bash
docker-compose -f docker-compose-pytap-PRD.yaml down
docker-compose -f docker-compose-pytap-PRD.yaml up --build -d --force-recreate