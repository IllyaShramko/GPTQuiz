#!/bin/bash
set -e  
mkdir -p ./library_app/static/images/questions

flask --app project db upgrade

exec gunicorn \
    --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
    --workers 1 \
    --bind 0.0.0.0:$PORT \
    wsgi:project
