from __future__ import absolute_import
import os
from time import timezone
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drones.settings')
app = Celery('drones')

app.conf.task_serializer = 'json'
app.conf.enable_utc = False
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone=settings.TIME_ZONE,
    enable_utc=True,
)
app.config_from_object(settings, namespace="CELERY")

# Celery Beat Settings
app.conf.beat_schedule = {
    # Executes.
    'task_drone_battery_capacity_check_each_x_min': {
        'task': 'drone_delivery.tasks.task_drone_battery_capacity_check',
        'schedule': crontab(minute=f"*/{settings.DRONE_DELIVERY_CONFIG['BATTERY_STATUS_UPDATE_TIME']}"),
    },
}
app.autodiscover_tasks()