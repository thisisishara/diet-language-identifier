#!/bin/bash

# Parse command-line arguments
confirm="false"
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -y)
    confirm="true"
    shift # past argument
    ;;
    -m|--model-version)
    MODEL_VERSION="$2"
    shift # past argument
    shift # past value
    ;;
    -b|--bucket-name)
    BUCKET_NAME="$2"
    shift # past argument
    shift # past value
    ;;
    -p|--project-name)
    PROJECT_NAME="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    echo "Unknown option: $key"
    exit 1
    ;;
  esac
done

# Read the value of MODEL_VERSION and PROJECT_NAME from the .env file
if [ -z "$MODEL_VERSION" ]
then
    MODEL_VERSION=$(grep -o 'MODEL_VERSION=[^[:blank:]]*' .env | cut -d '=' -f2)
fi
if [ -z "$PROJECT_NAME" ]
then
    PROJECT_NAME=$(grep -o 'PROJECT_NAME=[^[:blank:]]*' .env | cut -d '=' -f2)
fi
if [ -z "$BUCKET_NAME" ]
then
    BUCKET_NAME=$(grep -o 'BUCKET_NAME=[^[:blank:]]*' .env | cut -d '=' -f2)
fi

# Check if the file already exists in S3
if aws s3 ls "s3://${BUCKET_NAME}/${PROJECT_NAME}/lang-identifier-${MODEL_VERSION}.tar.gz"; then
  # Check if the file exists locally
  if [ -f "lang-identifier-${MODEL_VERSION}.tar.gz" ]; then
    if [[ "$confirm" == "true" ]]; then
      echo "A model with the same version tag is available locally and it will be overwritten"
    else
      read -rp "The file already exists locally. Do you want to overwrite it? (y/n): " choice
        case "$choice" in
          y|Y|yes|YES ) confirm="true";;
          n|N|no|NO ) confirm="false";;
          * ) echo "Invalid choice. Aborting."; exit 1;;
        esac
    fi
  else
    confirm="true"
  fi
else
  echo "Error: File not found in the bucket or invalid"
  exit 1
fi

# Downloading the file from S3
if [[ "$confirm" == "true" ]]; then
  if aws s3 cp "s3://${BUCKET_NAME}/${PROJECT_NAME}/lang-identifier-${MODEL_VERSION}.tar.gz" "lang-identifier-${MODEL_VERSION}.tar.gz"; then
    echo "Model download successfully."
  else
    echo "Model download unsuccessful."
    exit 1
  fi
else
  echo "Model download operation aborted."
  exit 1
fi
