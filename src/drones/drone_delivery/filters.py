from django.db.models import fields
from django_filters.rest_framework import (FilterSet, NumberFilter)

from .models import (Drone, Medication)

class DroneFilter(FilterSet):
    weight_limit_gte = NumberFilter(field_name="weight_limit", lookup_expr='gte')
    weight_limit_lte = NumberFilter(field_name="weight_limit", lookup_expr='lte')
    battery_capacity_lte = NumberFilter(field_name="battery_capacity", lookup_expr="lte")
    battery_capacity_gte = NumberFilter(field_name="battery_capacity", lookup_expr="gte")

    class Meta:
        model = Drone
        fields = ["slug", "serial_number", "model", "weight_limit", "battery_capacity", "state"]

class MedicationFilter(FilterSet):
    weight_gte = NumberFilter(field_name="weight", lookup_expr="gte")
    weight_lte = NumberFilter(field_name="weight", lookup_expr="lte")

    class Meta:
        model = Medication
        fields = ["slug", "name", "weight", "code"]
