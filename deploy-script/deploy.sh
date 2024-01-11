#!/bin/bash

# Variables - replace these with your actual data
USERNAME="orangepi"
ORANGEPI_IP="192.168.100.169"
REPO_PATH="~/apps/life-manager-app/"
DOCKER_IMAGE_NAME="life-manager-app"
GITHUB_REPO_URL="git@github.com:MatheusBLopes/life-manager-app.git"

# SSH into the Orange Pi
ssh $USERNAME@$ORANGEPI_IP << EOF

    # Pull the latest commits from GitHub
    echo "Pulling latest commits from GitHub repository..."
    cd $REPO_PATH
    git pull

    # Build the Docker image
    echo "Building Docker image..."
    docker build -t $DOCKER_IMAGE_NAME .

    # Stop and remove old containers
    docker stop life-manager-app && docker rm life-manager-app

    # Run the Docker image
    echo "Running Docker image..."
    docker run -d --network=main-net --name $DOCKER_IMAGE_NAME --env-file ./.env -p 9000:9000 $DOCKER_IMAGE_NAME

    echo "Removing old images.."
    docker image prune --filter "dangling=true" --force
EOF
