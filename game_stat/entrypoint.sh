#!/bin/sh

gunicorn  -t 30 -w 3 --error-logfile /logs/${HOSTNAME}-error.log --access-logfile /logs/${HOSTNAME}-access.log --capture-output -b 0.0.0.0:8003 wsgi:app
