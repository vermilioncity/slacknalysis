#!/bin/bash

set -ex

if [ "$#" -ne 0 ]; then
    exec "$@"
elif [ "$SUPERSET_ENV" = "development" ]; then
    FLASK_ENV=development FLASK_APP=superset flask run -p 8088 --with-threads --reload --debugger --host=0.0.0.0
elif [ "$SUPERSET_ENV" = "production" ]; then
    ECHO "figure this out later"
else
    superset --help
fi
