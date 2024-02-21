#!/bin/bash
docker-compose -f docker-compose-pytap-dev.yaml down
docker-compose -f docker-compose-pytap-dev.yaml up --build -d --force-recreate