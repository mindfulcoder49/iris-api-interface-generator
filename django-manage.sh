#!/bin/sh
# Move to the app directory
cd /irisdev/app/app

# Apply migrations and setup superuser
python3 manage.py "$@"
