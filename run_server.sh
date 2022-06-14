#!/bin/sh
git pull --no-rebase
gunicorn "app:create_app()" --workers 2 --threads 2 -b 0.0.0.0:8000
