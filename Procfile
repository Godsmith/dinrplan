release: python manage.py migrate
web: daphne --port $PORT --bind 0.0.0.0 dinrplan.asgi:application
