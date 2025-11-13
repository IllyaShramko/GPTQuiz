web: sh -c "
  echo 'Создание директорий...';
  mkdir -p ./library_app/static/images/questions;

  echo 'Применение миграций...';
  flask --app project db upgrade;

  echo 'Запуск Gunicorn...';
  gunicorn \
    --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
    --workers 1 \
    --bind 0.0.0.0:$PORT \
    wsgi:project
"
