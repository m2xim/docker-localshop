#!/bin/bash

set -e

#Params
# LOCALSHOP_USERNAME localshop
# LOCALSHOP_PASSWORD localshop
# LOCALSHOP_EMAIL admin@localshop.example.org

# LOCALSHOP_ACCESS_KEY
# LOCALSHOP_SECRET_KEY

# LOCALSHOP_CIDR_VALUE 0.0.0.0/0
# LOCALSHOP_CIDR_REQUIRE_CREDENTIALS 1
# LOCALSHOP_CIDR_LABEL everyone

# LOCALSHOP_DATABASE_ENGINE django.db.backends.sqlite3
# LOCALSHOP_DATABASE_NAME /home/localshop/data/localshop.db
# LOCALSHOP_DATABASE_USER
# LOCALSHOP_DATABASE_PASSWORD
# LOCALSHOP_DATABASE_HOST
# LOCALSHOP_DATABASE_PORT
# LOCALSHOP_TIMEZONE America/Montreal
# LOCALSHOP_DELETE_FILES False

cd /home/localshop

fab localshop_init

source /home/localshop/venv/bin/activate
localshop run_gunicorn 0.0.0.0:8000 &
localshop celeryd -B -E