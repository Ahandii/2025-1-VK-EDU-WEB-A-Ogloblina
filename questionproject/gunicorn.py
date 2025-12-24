# gunicorn --workers 3 --bind 0.0.0.0:8000 myproject.wsgi:application
# gunicorn -c /etc/gunicorn.conf.py myproject.wsgi:application
import multiprocessing
# gunicorn.conf.py

# The socket to bind
bind = "127.0.0.1:8000"

# Number of worker processes (recommended: (2 x $num_cores) + 1)
#workers = 3
workers = multiprocessing.cpu_count() * 2 + 1

# accesslog = "./var/log/gunicorn/access.log"
# errorlog = "./var/log/gunicorn/error.log"
# loglevel = "info"