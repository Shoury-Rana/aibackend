#!/bin/bash
# build_files.sh

echo "BUILD START"

# Ensure pip is up to date (optional but good practice)
python3.9 -m pip install --upgrade pip

# Install dependencies
python3.9 -m pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput --clear

echo "BUILD END"

# Note: Vercel automatically handles migrations for simple setups if needed,
# but for complex apps or specific needs, you might add migration commands here.
# python3.9 manage.py makemigrations --noinput
# python3.9 manage.py migrate --noinput