web: gunicorn streamsavvy_dataprocessing.wsgi --log-file -
celery: ./manage.py celeryd --verbosity=2 --loglevel=INFO
celery_beat: ./manage.py celerybeat --verbosity=2 --loglevel=DEBUG
migrate: ./manage.py
