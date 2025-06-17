#!/bin/bash

# Exit on error
set -e

# Run reset and schema creation
./scripts/standalone/001_reset_db.sh
./scripts/standalone/002_create_schema.sh
./scripts/standalone/003_et_data.sh
./scripts/standalone/004_load_data.sh