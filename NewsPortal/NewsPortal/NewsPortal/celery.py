import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_weekly_news': {
        'task': 'news.tasks.weekly_news',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
        'args': (),
    },
}
app.autodiscover_tasks()