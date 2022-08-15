web: gunicorn techtest.techtest.wsgi -b 0.0.0.0:$PORT
heroku ps:scale web=1
python manage.py migrate
