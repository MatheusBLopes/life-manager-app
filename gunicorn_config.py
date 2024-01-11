import os

worker_class = "gevent"
workers = int(os.environ.get("WORKERS", "1"))
threads = int(os.environ.get("THREADS", "1"))

bind = "0.0.0.0:9000"
worker_tmp_dir = "/dev/shm"
chdir = "life-manager-app"
max_requests = int(os.environ.get("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.environ.get("GUNICORN_MAX_REQUESTS_JITTER", "25"))
graceful_timeout = 30
