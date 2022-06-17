#!/bin/sh
git pull --no-rebase
python pull_data.py
gunicorn "app:create_app()" --workers 2 --threads 2 -b 0.0.0.0:8000
