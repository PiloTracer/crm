#!/bin/bash
sudo docker-compose -f docker-compose-rabbitmq.yaml down
sudo docker-compose -f docker-compose-rabbitmq.yaml up --build -d --force-recreate