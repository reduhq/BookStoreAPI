#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=api \
SMTP_HOST="" \
VOLUME_NAME=test-db-data \
INSTALL_DEV=true \
docker compose \
-f docker-compose.yml \
config > docker-stack.yml

docker compose -f docker-stack.yml build
if docker volume ls | grep -q 'schoolapi_test-db-data'; then
    docker compose -f docker-stack.yml down -v --remove-orphans
else
    docker compose -f docker-stack.yml down --remove-orphans # 
fi
# docker volume rm schoolapi_test-db-data Remove possibly previous broken stacks left hanging after an error
docker compose -f docker-stack.yml up -d
sleep 10
docker compose -f docker-stack.yml exec -T api bash /SchoolApi/test_start.sh "$@"
docker compose -f docker-stack.yml down -v --remove-orphans