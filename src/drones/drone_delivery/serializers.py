from rest_framework import serializers
from .models import (Drone)

class DroneSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        instance.battery_capacity = validated_data.get("battery_capacity", instance.battery_capacity)
        instance.state = validated_data.get("state", instance.state)
        return instance

    def create(self, validated_data):
        return Drone(**validated_data)
        
    class Meta:
        model = Drone
