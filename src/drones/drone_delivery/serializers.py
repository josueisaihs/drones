from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db.models import Q

from . import queryset

from .models import (
    Drone, 
    Medication, 
    DeliveryPackage
)

class DroneSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.serial_number = validated_data.get("serial_number", instance.serial_number)
        instance.model = validated_data.get("weight_limit", instance.weight_limit)
        instance.weight_limit = validated_data.get("weight_limit", instance.weight_limit)
        instance.battery_capacity = validated_data.get("battery_capacity", instance.battery_capacity)
        instance.state = validated_data.get("state", instance.state)
        instance.save()

        return instance

    def create(self, validated_data):
        return Drone.objects.create(**validated_data)

    def validate(self, data):
        if int(data["battery_capacity"]) < 0 or 100 < int(data["battery_capacity"]):
            raise serializers.ValidationError({"battery_capacity": _(f"The value {data['battery_capacity']} for the Battery Capacity is wrong. Battery Capacity must be value between 0 and 100")})

        if float(data["weight_limit"]) < 0. or 500. < float(data["weight_limit"]):
            raise serializers.ValidationError({"weight_limit": _(f"The value {data['weight_limit']} as Weight Limit is wrong. The value must be a maximum of 500g.")})
        
        return data

    class Meta:
        model = Drone
        fields = ["slug", "serial_number", "model", "weight_limit", "battery_capacity", "state"]
        validators = []


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["slug", "name", "weight", "code", "image"]


class DeliveryPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPackage
        fields = ["drone", "medications", "slug"]