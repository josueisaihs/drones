from django.db.models import QuerySet
from django.db.models import Q
from django.conf import settings

class DroneQuerySet(QuerySet):
    def low_battery(self):
        return self.filter(battery_capacity__lte = 25)

    def with_sufficient_battery(self):
        return self.filter(battery_capacity__gt = 25)

    def loading_status(self):
        return self.filter(state = "LOADING")

class DeliveryPackageQuerySet(QuerySet):
    def canLoad(self):
        return self.filter(Q(drone__state = "IDLE") & Q(drone__battery_capacity__gte = settings.DRONE_DELIVERY_CONFIG["LOW_BATTERY"]))

class PackageQuerySet(QuerySet):
    pass