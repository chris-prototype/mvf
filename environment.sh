#!/bin/bash

# environment
# environment is implemented as a docker container
# the script builds and agent image and runs a container containing claude code

# build the agent image
docker build -f .devcontainer/Dockerfile.agent -t factory-agent .

# run the container and check claude version in the container
docker run --rm factory-agent claude --version
