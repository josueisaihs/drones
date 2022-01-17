import re

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
    """
    INPUT
    {
        "serial_number": <String>,
        "model": <String: Cruiserweight, Lightweight, "Middleweight, Cruiserweight, Heavyweight>,
        "weight_limit": <Float>,
        "battery_capacity": <Int>,
        "state": <String: IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING>
    }

    OUTPUT
    {
        "slug": <String>,
        "serial_number": <String>,
        "model": <String: Cruiserweight, Lightweight, "Middleweight, Cruiserweight, Heavyweight>,
        "weight_limit": <Float>,
        "battery_capacity": <Int>,
        "state": <String: IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING>
    }
    """

    def validate(self, data):
        # The battery capacity must be between 0 and 100% 
        if int(data["battery_capacity"]) < 0 or 100 < int(data["battery_capacity"]):
            raise serializers.ValidationError({"battery_capacity": _(f"The value {data['battery_capacity']} for the Battery Capacity is wrong. Battery Capacity must be value between 0 and 100")})

        # The weight limit must be positive and less than or equal to settings.DRONE_DELIVERY_CONFIG["MAX_WEIGHT"], default value is 500g
        if float(data["weight_limit"]) < 0. or settings.DRONE_DELIVERY_CONFIG["MAX_WEIGHT"] < float(data["weight_limit"]):
            raise serializers.ValidationError({"weight_limit": _(f"The value {data['weight_limit']} as Weight Limit is wrong. The value must be a maximum of {settings.DRONE_DELIVERY_CONFIG['MAX_WEIGHT']}g.")})
        
        return data

    class Meta:
        model = Drone
        fields = ["id", "slug", "serial_number", "model", "weight_limit", "battery_capacity", "state"]
        read_only_fields = ('slug',)
        lookup_field = ('slug',)
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class MedicationSerializer(serializers.ModelSerializer):
    """
    INPUT
    {
        "name": <String>,
        "weight": <Float>,
        "code": <String>,
        "image": <Image>
    }

    OUTPUT
    {
        "slug": <Slug>,
        "name": <String>,
        "weight": <Float>,
        "code": <String>,
        "image": <URL>
    }
    """

    def _code_validation_(self, value):
        # Allowed only upper case letters [A-Z], underscore ['_'] and numbers [0-9]
        # Note: The regular expression would be ^[A-Z0-9_-]*$, but I wanted to show another way
        allows_characters = [chr(i) for i in range(65, 91)] + list(map(str, range(0, 10))) + ["_",]
        return all([_chr_ in allows_characters for _chr_ in value])

    def _name_validation_(self, value):        
        # Allowed only letters [A-Za-z], numbers[0-9], ‘-‘, ‘_’
        return re.match(r'^[A-Za-z0-9_-]*$', value)

    def validate(self, data):
        if not self._name_validation_(data["name"]):
            raise serializers.ValidationError(
                {
                    "name": _(f"The name {data['name']} contains characters not allowed, allowed only letters, numbers, '-', '_'")
                }
            )

        if not self._code_validation_(data["code"]):
            raise serializers.ValidationError(
                {
                    "code": _(f"The code '{data['code']}' contains characters not allowed, allowed only upper case letters, underscore and numbers."),
                }
            )

        # Validate that the weight of the medication can be carried by the drone
        if data["weight"] > settings.DRONE_DELIVERY_CONFIG["MAX_WEIGHT"]:
            raise serializers.ValidationError(
                {
                    "weight": _(f"The value must be a maximum of {settings.DRONE_DELIVERY_CONFIG['MAX_WEIGHT']}g.")
                }
            )
        return data

    class Meta:
        model = Medication
        fields = ["id", "slug", "name", "weight", "code", "image"]
        read_only_fields = ('slug',)
        lookup_field = ('slug',)
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class PackageSerializer(serializers.ModelSerializer):
    '''
    INPUT 
    {
        "medication": <Medication.pk>,
        "qty": <Int>
    }

    OUTPUT
    {
        "slug": <Slug>,
        "medication": {<Medication(name, slug)>},
        "qty": <Int>,
        "created": "%y-%m-%d %H:%M",
        "weight": <Float>
    }
    '''

    class Meta:
        model = Package
        fields = ["id", "slug", "medication", "qty", "created"]
        read_only_fields = ('slug', "created")
        lookup_field = ('slug',)
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def _date_time_formater_(self, S):
        date, time = S.split("T")
        y, m, d = date.split("-")
        tt = time.split(":")

        return f"{y}-{m}-{d} {tt[0]}:{tt[1]}"

    def to_representation(self, instance):
        package = super().to_representation(instance)
        medication = Medication.objects.get(id = package["medication"])
        package['weight'] = medication.weight * package["qty"]
        package["medication"] = {"name": medication.name, "slug": medication.slug}
        package["created"] = self._date_time_formater_(package["created"])

        return package

    def validate(self, data):
        medication_weight = data["medication"].weight
        qty = data["qty"]

        weight = medication_weight * qty

        if weight > settings.DRONE_DELIVERY_CONFIG["MAX_WEIGHT"]:
            raise serializers.ValidationError(
                {
                    "qty": _(f"The weight {weight}g of the package exceeds the maximum limit ({settings.DRONE_DELIVERY_CONFIG['MAX_WEIGHT']}g) that the drones can carry")
                }
            )

        return super().validate(data)

class DeliveryPackageSerializer(serializers.ModelSerializer):
    '''
    INPUT
    {
        "drone": <Drone.pk>
        "pacakge": [<Package.pk>, <Package.pk>, ..., <Package.pk>]
    }

    OUTPUT
    {
        "slug": <Slug>,
        "drone": <Drone(slug, serial_number, weight_limit, battery_capacity)>,
        "package": {
            "items": [
                <Package(slug, weight, qty, 
                    <Medication(slug, name)>
                )>,
                <Package(slug, weight, qty, 
                    <Medication(slug, name)>
                )>,
                ...
                <Package(slug, weight, qty, 
                    <Medication(slug, name)>
                )>,
            ],
            "weight": <Float> # Total Weight Package
        }
    }
    '''
    class Meta:
        model = DeliveryPackage
        fields = ["slug", "drone", "package"]
        read_only_fields = ('slug',)
        lookup_field = ('slug',)
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

        # Depth = 2 can be used to display the nested models, 
        # but I prefer to use to_representation to only display the necessary data
        # depth = 2

    def to_representation(self, instance):
        delivery = super().to_representation(instance)

        # Change drone representation
        drone = Drone.objects.get(id = delivery["drone"])
        delivery["drone"] = {
            "slug": drone.slug, 
            "serial_number": drone.serial_number,
            "weight_limit": drone.weight_limit,
            "battery_capacity": drone.battery_capacity
        }

        packages = Package.objects.filter(id__in = delivery["package"])
        weight = 0 

        _packages_ = []
        for package in packages:
            package_weight = package.qty * package.medication.weight
            weight = weight + package_weight
            _packages_.append({
                "slug": package.slug,
                "weight": package_weight,
                "qty": package.qty,
                "medication": {
                    "slug": package.medication.slug,
                    "name": package.medication.name
                }
            })

        # Change package representation
        delivery["package"] = {
            "items": _packages_,
            "weight": weight
        }

        return delivery

    def create(self, validated_data):
        delivery = DeliveryPackage()
        delivery.drone = validated_data["drone"]
        delivery.save()
        delivery.package.set(validated_data["package"])
        delivery.save()

        # Change drone state from IDLE to LOADING
        drone = Drone.objects.get(slug = delivery.drone.slug)
        drone.state = "LOADING"
        drone.save()

        return delivery
    
    def validate(self, data):
        # Validate that the weight of the package is not greater than the maximum weight that the drone supports
        drone_state = data["drone"].state
        drone_battery = data["drone"].battery_capacity
        drone_weight_limit = data["drone"].weight_limit
        packages_weight = sum([package.qty * package.medication.weight for package in data["package"]])

        if drone_state != "IDLE":
            raise serializers.ValidationError(
                {
                    "drone": _(f"The drone {data['drone'].serial_number} is busy")
                }
            )
        
        if drone_battery < settings.DRONE_DELIVERY_CONFIG["LOW_BATTERY"]:
            raise serializers.ValidationError(
                {
                    "drone": _(f"The drone has low battery. The battery is under {settings.DRONE_DELIVERY_CONFIG['LOW_BATTERY']}")
                }
            )
        
        if packages_weight == 0:
            raise serializers.ValidationError(
                {
                    "package": _("The package must contain at least one element.")
                }
            )
        if drone_weight_limit < packages_weight:
            raise serializers.ValidationError(
                {
                    "drone": _(f"The drone does not support that weight. Its max. weight is {drone_weight_limit}g and the package weight is {packages_weight}g.")
                }
            )

        return data