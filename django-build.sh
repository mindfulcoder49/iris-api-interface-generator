#!/bin/bash

# Optionally install Python dependencies (uncomment if necessary)
/irisdev/app/install-python-deps.sh

# Run Django migrations and create the superuser
/irisdev/app/django-manage.sh makemigrations
/irisdev/app/django-manage.sh migrate
# Collect static files
/irisdev/app/django-manage.sh collectstatic --no-input --clear

# Reload the IRIS production
/irisdev/app/reload-production.sh