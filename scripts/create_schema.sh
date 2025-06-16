#!/bin/bash

# Exit on error
set -e

# Load variables from .env
set -o allexport
source .env
set +o allexport

# Run schema creation script on the newly created database
psql -U "$DB_USER" -d "$DB_NAME" -f sql/schema.sql