#!/bin/bash

set -e

echo "Fetching repo updates"
git pull

echo "Building and lanuching containers"
sudo docker-compose build
sudo docker-compose up -d

echo "Removing unused images and containers"
docker system prune -f

echo "Project deployed successfully"