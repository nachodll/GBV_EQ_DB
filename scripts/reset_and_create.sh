#!/bin/bash

# Exit on error
set -e

# Run reset and schema creation
./scripts/reset_db.sh
./scripts/create_schema.sh