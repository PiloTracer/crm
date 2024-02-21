docker-compose -f docker-compose-dashboard-dev.yaml down
docker-compose -f docker-compose-dashboard-dev.yaml build --no-cache
docker-compose -f docker-compose-dashboard-dev.yaml up -d --force-recreate
