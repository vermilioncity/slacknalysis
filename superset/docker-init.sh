#!/bin/bash

set -ex

export FLASK_APP=superset
export SUPERSET_CONFIG_PATH=superset_config.py

superset fab create-admin --username superset --password password --email rbruehlman@gmail.com --firstname rebecca --lastname bruehlman

superset db upgrade

superset init

superset run -p 8088 --with-threads --reload --debugger
