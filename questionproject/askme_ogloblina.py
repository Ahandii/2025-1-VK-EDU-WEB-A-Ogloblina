# gunicorn --workers 3 --bind 0.0.0.0:8000 myproject.wsgi:application
# gunicorn -c /etc/gunicorn.conf.py myproject.wsgi:application
import multiprocessing

bind = "127.0.0.1:8000"

workers = 2

daemon = False