#!/bin/sh

# Set the network name
NETWORK_NAME="external_network"

# Check if the network already exists
if docker network ls | grep -q "$NETWORK_NAME"; then
    echo "Network $NETWORK_NAME already exists."
else
    # Create the network
    sudo docker network create "$NETWORK_NAME"
    echo "Network $NETWORK_NAME created successfully."
fi