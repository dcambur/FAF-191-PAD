#!/bin/sh

gunicorn -t 30 -w 1 --error-logfile /logs/${HOSTNAME}-error.log --access-logfile /logs/${HOSTNAME}-access.log --capture-output -b 0.0.0.0:8004 wsgi:app