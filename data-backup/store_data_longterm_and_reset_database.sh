#!/bin/bash

PYTHON_FILE="extract_from_database.py"

if [[ -f "$PYTHON_FILE" ]]; then
    echo "Running $PYTHON_FILE..."
    python3.9 "$PYTHON_FILE"
else
    echo "Error: $PYTHON_FILE not found!"
    exit 1
fi

sqlcmd -S $DB_HOST -U $DB_USER -P $DB_PASSWORD -d $DB_NAME -i ../schema.sql