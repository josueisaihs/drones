from django.db.models import QuerySet

class DroneQuerySet(QuerySet):
    def low_battery(self):
        return self.filter(battery_capacity__lte = 25)

    def with_sufficient_battery(self):
        return self.filter(battery_capacity__gt = 25)

    def loading_status(self):
        return self.filter(state = "LOADING")