#!/bin/sh

cd "$(dirname $(realpath $0))"
VENV="$(pipenv --venv)"
WSGI_FILE="$(pwd)/sabot/wsgi.py"

exec uwsgi --die-on-term --need-plugin python3 --virtualenv "$VENV" --wsgi-file "$WSGI_FILE" --pythonpath "$(pwd)" --master --processes 2 --threads 8 --http-socket :9090

