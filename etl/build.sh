#!/bin/bash

# Define an array of your service names
services=("extract" "transform" "load")

# Loop over the services
for service in "${services[@]}"
do
    # Build the Docker image
    docker build -t $service ./$service
done