import os

bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")
workers = os.environ.get("GUNICORN_WORKERS", "3")
accesslog = os.environ.get("GUNICORN_ACCESS_LOG", "-")
errorlog = os.environ.get("GUNICORN_ERROR_LOG", "-")
capture_output = True
