web: gunicorn core.wsgi --log-file -
worker: celery worker --app=tasks.app