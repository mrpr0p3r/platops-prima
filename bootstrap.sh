#!/bin/sh
export FLASK_APP=./index.py
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pipenv install marshmallow flask sqlalchemy psycopg2
pipenv run flask --debug run -h 0.0.0.0
