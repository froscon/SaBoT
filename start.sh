#!/bin/bash
touch gunicorn.log
touch access.log

tail -n 0 -f *.log &

echo Starting Gunicorn.
exec gunicorn sabot.wsgi:application \
    --bind 0.0.0.0:8000 \
    --name sabot \
    --workers 3 \
    --log-level=info \
    --log-file=/sabot/gunicorn.log \
    --access-logfile=/sabot/access.log \
    "$@"
