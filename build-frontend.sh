#!/bin/sh
# Build the frontend
cd /irisdev/app/app/frontend
npm install
npm run build

cd /irisdev/app/app
python3 manage.py collectstatic --noinput

# Move to the app directory
cd /irisdev/app

bash reload-production.sh
