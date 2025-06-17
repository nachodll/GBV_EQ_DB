#!/bin/bash

# Exit on error
set -e

# Load variables from .env
set -o allexport
source .env
set +o allexport

# Create a temporary SQL file
TEMP_SQL=$(mktemp)

# Substitute .env variables in the reset template into the temporary file
envsubst < sql/reset_db_template.sql > "$TEMP_SQL"

# Drop and recreate the database
psql -U postgres -f "$TEMP_SQL"

# Delete the temporary file
rm -f "$TEMP_SQL"