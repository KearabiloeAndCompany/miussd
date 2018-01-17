release: python manage.py migrate --no-input
web: gunicorn BookingPlatform.wsgi --preload --log-file -