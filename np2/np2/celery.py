import os
from celery import Celery
import dotenv
from .settings import BASE_DIR
from celery.schedules import crontab

env_file = os.path.join(BASE_DIR, '.env')
dotenv.read_dotenv(env_file)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'np2.settings')

app = Celery('np2')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# This is to fix a known celery bug with crontab and timezones
app.conf.enable_utc = False
app.conf.timezone = "Europe/Moscow"

app.conf.beat_schedule = {
    'weekly_newsletter_async': {
        'task': 'news.tasks.weekly_newsletter_async',
        'schedule': crontab(minute='0', hour='8', day_of_week='monday'),
    },
}
