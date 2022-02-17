#! /bin/sh 

set -e 

python3 ./manage.py migrate 
python3 ./manage.py createsuperuser --no-input --email $DJANGO_ADMIN_EMAIL --username $DJANGO_ADMIN_USERNAME || true
python3 ./manage.py runserver 0.0.0.0:8000
