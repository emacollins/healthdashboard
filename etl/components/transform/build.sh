#!/bin/bash

# Define an array of your service names
services=("healthdashboard/etl/transform")

account_number=$(aws sts get-caller-identity --query Account --output text)

region=$(aws configure get region)

# Get the ECR login password and login to Docker
aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${account_number}.dkr.ecr.${region}.amazonaws.com

# Loop over the services
for service in "${services[@]}"
do
    # Build the Docker image
    docker build -t $service .

    # Tag the Docker image
    docker tag $service:latest ${account_number}.dkr.ecr.${region}.amazonaws.com/$service:latest

    # Push the Docker image to ECR
    docker push ${account_number}.dkr.ecr.${region}.amazonaws.com/$service:latest
done