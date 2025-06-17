#!/bin/bash

# Stop script on any error
set -e

# Load variables from .env
set -o allexport
source .env
set +o allexport

# Run the Python orchestration script
python pipelines/extract_transform/000_et_all.py