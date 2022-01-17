from django.conf import settings

from celery.utils.log import get_task_logger
from celery import shared_task

from .models import Drone

logger = get_task_logger(__name__)

@shared_task(bind = True)
def task_drone_battery_capacity_check(attr):
    """
    Update the battery status of each drone every so often
    """
    if settings.DEBUG:
        for drone in Drone.objects.are_working():
            if drone.battery_capacity > 0:
                drone.battery_capacity = drone.battery_capacity - 1
                logger.info(f"Update drone {drone.serial_number} ({drone.battery_capacity}%)")
                drone.save()
            else:
                logger.info(f"Drone {drone.serial_number} ({drone.battery_capacity}%) need charge")
    else:
        pass