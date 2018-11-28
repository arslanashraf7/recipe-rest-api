#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/arslanashraf7/recipe-rest-api.git'

PROJECT_BASE_PATH='/usr/local/apps'
VIRTUALENV_BASE_PATH='/usr/local/virtualenvs'

# Set Ubuntu Language
locale-gen en_GB.UTF-8

# Install Python, SQLite and pip
echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH/recipe-rest-api

mkdir -p $VIRTUALENV_BASE_PATH
python3 -m venv $VIRTUALENV_BASE_PATH/recipe_api

$VIRTUALENV_BASE_PATH/recipe_api/bin/pip install -r $PROJECT_BASE_PATH/recipe-rest-api/requirements.txt

# Run migrations
cd $PROJECT_BASE_PATH/recipe-rest-api/src

# Setup Supervisor to run our uwsgi process.
cp $PROJECT_BASE_PATH/recipe-rest-api/deploy/supervisor_recipe_api.conf /etc/supervisor/conf.d/recipe_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart recipe_api

# Setup nginx to make our application accessible.
cp $PROJECT_BASE_PATH/recipe-rest-api/deploy/nginx_recipe_api.conf /etc/nginx/sites-available/recipe_api.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/recipe_api.conf /etc/nginx/sites-enabled/recipe_api.conf
systemctl restart nginx.service

echo "DONE! :)"
