#!/bin/bash

echo -n "Please enter your DB password: "
read -s password
echo

# Clear out the schema
mysqladmin -u root -p"$password" drop -f dev-fnf-signup 2>/dev/null
mysqladmin -u root -p"$password" create -f dev-fnf-signup 2>/dev/null

# Kill old migrations
rm signup/migrations/*

# Do initial migration
python ./manage.py migrate 
python ./manage.py makemigrations signup 
python ./manage.py migrate signup 

# Create a superuser
echo "Creating superuser maximus..."
python ./manage.py createsuperuser --username maximus --email 'maximus@fatboycentral.com'


