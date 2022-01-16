from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from django.conf import settings

from .models import (
    Drone, 
    Medication, 
    DeliveryPackage,
    Package
)

class DroneSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Drone.objects.update_or_create(**validated_data)

    def validate(self, data):
        if int(data["battery_capacity"]) < 0 or 100 < int(data["battery_capacity"]):
            raise serializers.ValidationError({"battery_capacity": _(f"The value {data['battery_capacity']} for the Battery Capacity is wrong. Battery Capacity must be value between 0 and 100")})

        # The weight limit must be positive and less than or equal to settings.DRONE_DELIVERY_CONFIG["MAX_WEIGHT"], default value is 500g
        if float(data["weight_limit"]) < 0. or settings.DRONE_DELIVERY_CONFIG["MAX_WEIGHT"] < float(data["weight_limit"]):
            raise serializers.ValidationError({"weight_limit": _(f"The value {data['weight_limit']} as Weight Limit is wrong. The value must be a maximum of {settings.DRONE_DELIVERY_CONFIG['MAX_WEIGHT']}g.")})
        
        return data

    class Meta:
        model = Drone
        fields = ["slug", "serial_number", "model", "weight_limit", "battery_capacity", "state"]


class MedicationSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # Validate that the weight of the medication can be carried by the drone
        if data["weight"] > settings.DRONE_DELIVERY_CONFIG["MAX_WEIGHT"]:
            raise serializers.ValidationError({"weight": _(f"The value must be a maximum of {settings.DRONE_DELIVERY_CONFIG['MAX_WEIGHT']}g.")})
        return data
    class Meta:
        model = Medication
        fields = ["slug", "name", "weight", "code", "image"]


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ["slug", "medication", "qty"]

    def create(self, validated_data):
        return Package.objects.update_or_create(**validated_data)

class DeliveryPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPackage
        fields = ["drone", "package", "slug"]

    def create(self, validated_data):
        return DeliveryPackage.objects.update_or_create(**validated_data)
    
    def validate(self, data):
        # todo: Validate that the weight of the package can be carried by the drone
        # Validate that the weight of the package is not greater than the maximum weight that the drone supports
        # drone_weight_limit = data["drone"].weight_limit
        # package_weight = sum([medication.weight for medication in data["medications"]])
        # if drone_weight_limit < package_weight:
        #     raise serializers.ValidationError({"drone": _("The drone does not support that weight")})

        return data