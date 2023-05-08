#!/bin/bash

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -p|--project-name)
    PROJECT_NAME="$2"
    shift # past argument
    shift # past value
    ;;
    -b|--bucket-name)
    BUCKET_NAME="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    echo "Unknown option: $key"
    exit 1
    ;;
  esac
done

# If PROJECT_NAME not set from command-line argument, read from .env file
if [ -z "$PROJECT_NAME" ]
then
  PROJECT_NAME=$(grep -w PROJECT_NAME "$(dirname "$0")/.env" | cut -d '=' -f2)
fi
if [ -z "$BUCKET_NAME" ]
then
    BUCKET_NAME=$(grep -o 'BUCKET_NAME=[^[:blank:]]*' .env | cut -d '=' -f2)
fi

# Use the PROJECT_NAME environment variable in the aws command and capture the output
output=$(aws s3 ls "s3://${BUCKET_NAME}/${PROJECT_NAME}/")

# Check if the output is empty
if [ -z "$output" ]; then
  echo "No models found for $PROJECT_NAME/"
else
  echo "Models in $PROJECT_NAME/:"
  echo "$output"
fi
