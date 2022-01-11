from django_filters.rest_framework import (FilterSet, NumberFilter)

from .models import Drone

class DroneFilter(FilterSet):
    weight_limit_gte = NumberFilter(field_name="weight_limit", lookup_expr='gte')
    weight_limit_lte = NumberFilter(field_name="weight_limit", lookup_expr='lte')
    battery_capacity_lte = NumberFilter(field_name="battery_capacity", lookup_expr="lte")
    battery_capacity_gte = NumberFilter(field_name="battery_capacity", lookup_expr="gte")

    class Meta:
        model = Drone
        fields = ["serial_number", "model", "weight_limit", "battery_capacity", "state"]