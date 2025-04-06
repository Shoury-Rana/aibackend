#!/bin/bash
# build_files.sh

echo "BUILD START"

# Install dependencies (rely on pip being in PATH)
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files (rely on python being in PATH)
# Using 'python' is often safer as Vercel maps it to the correct version.
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "BUILD END"
