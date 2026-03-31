import multiprocessing

workers=2*multiprocessing.cpu_count()+1
worker_class='sync'
worker_connection=1000

timeout=30
graceful_timeout=30

max_request=1000
max_request_jitter=50

accesslog='gunicorn_access.log'
errorlog='gunicorn_error.log'
loglevel='info'

bind='0.0.0.0:7000'