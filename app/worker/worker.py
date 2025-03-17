import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()


app = Celery(
    'worker',
    broker=os.getenv('CELERY_BROKER'),
    backend=os.getenv('CELERY_BACKEND')
)

app.conf.update(
    result_expires=60 * 60 * 24,
    track_started=True
)

app.autodiscover_tasks(['app.worker.service'])
