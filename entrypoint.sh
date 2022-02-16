#! /bin/sh 

set -e 

python3 ./manage.py migrate 

if [ ! -f first-start ]; then 
    echo Running first-start tasks.
    echo username: $DJANGO_ADMIN_USERNAME
    echo email: $DJANGO_ADMIN_USERNAME
    echo password: $DJANGO_SUPERUSER_PASSWORD
    python3 ./manage.py createsuperuser --no-input --email $DJANGO_ADMIN_EMAIL --username $DJANGO_ADMIN_USERNAME
    touch first-start
fi 

python3 ./manage.py runserver 0.0.0.0:8000
