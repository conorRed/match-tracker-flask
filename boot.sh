#!/bin/sh
flask db upgrade
flask seed
exec gunicorn -b :5000 --access-logfile - --error-logfile - match-tracker:app
