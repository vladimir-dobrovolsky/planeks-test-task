web: gunicorn core.wsgi:application --log-file -
worker: celery --app core.celery worker