#!/bin/sh

# Optionally install Python dependencies (uncomment if necessary)
/irisdev/app/install-python-deps.sh

# Start IRIS and wait for it to be ready
/irisdev/app/start-iris.sh

# Reload the IRIS production
/irisdev/app/reload-production.sh

# Build the frontend
/irisdev/app/build-frontend.sh

# Run Django migrations and create the superuser
/irisdev/app/django-manage.sh makemigrations
/irisdev/app/django-manage.sh migrate

# Optionally create a Django superuser
export DJANGO_SUPERUSER_PASSWORD=SYS
/irisdev/app/django-manage.sh createsuperuser --no-input --username SuperUser --email admin@admin.fr

# Collect static files
/irisdev/app/django-manage.sh collectstatic --no-input --clear

# Optionally restart IRIS (uncomment if necessary)
# /irisdev/app/restart-iris.sh

# Keep the container running by tailing the IRIS log
iop --log
