from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','dvid.settings')

app = Celery('dvid')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request {self.request}')