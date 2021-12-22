#!/bin/bash
set -e
if [ "$CONTEXT" = 'DEV' ]; then
    echo "Running Development Server"
    exec python3 "/home/flask/app/monster_icon.py"
else
    echo "Running Production Server"
    exec uwsgi --http 0.0.0.0:9090 --wsgi-file /home/flask/app/monster_icon.py --callable app --stats 0.0.0.0:9191
fi
