import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')


app = Celery('bigcart',
             broker='amqp://',
             backend='rpc://',
             include=['bigcart.tasks'])

app.conf.update(
    result_expires=3600,
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()