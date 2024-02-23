#!/bin/bash
sudo docker compose -f docker-compose-couchdb.yaml down
sudo docker compose -f docker-compose-couchdb.yaml up --build -d --force-recreate