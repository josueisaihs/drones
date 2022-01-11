from rest_framework import serializers
from .models import (Drone)

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

    class Meta:
        model = Drone
        fields = "__all__"
