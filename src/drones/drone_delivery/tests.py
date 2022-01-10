import random

from django.db import IntegrityError
from django.test import TestCase

from .models import (Drone)

class DroneTestCase(TestCase):
    def random_data_generate(self):
        obj = {
            "serial_number": random.randrange(100000),
            "model": random.choice(("Lightweight", "Middleweight", "Cruiserweight", "Heavyweight")),
            "weight_limit": random.randrange(500),
            "battery_capacity": random.randrange(100),
            "state": random.choice(("IDLE", "LOADING", "LOADED", "DELIVERING", "DELIVERED", "RETURNING"))
        }
        return obj

    def setUp(self):
        for i in range(10):
            obj = self.random_data_generate()

            while Drone.objects.filter(serial_number = obj["serial_number"]).exists():
                obj = self.random_data_generate()

            drone = Drone(
                serial_number = obj["serial_number"],
                model = obj["model"],
                weight_limit = obj["weight_limit"],
                battery_capacity = obj["battery_capacity"],
                state = obj["state"]
            )
            drone.save()
    
    def test_create_company(self):
        drone = Drone.objects.all()

        _output_ = len(drone)
        _expected_ = 10

        self.assertEqual(_output_, _expected_)

    def test_low_battery_queryset(self):
        _output_ = Drone.objects.low_battery()
        _expected_ = Drone.objects.filter(battery_capacity__lte = 25)

        self.assertEqual(len(_output_), len(_expected_))

    def test_loading_status(self):
        _output_ = Drone.objects.loading_status()
        _expected_ = Drone.objects.filter(state = "LOADING")

        self.assertEqual(len(_output_), len(_expected_))

    def test_concatenated_queryset(self):
        _output_ = Drone.objects.low_battery()
        
    def test_drone_detail(self):
        drone = Drone.objects.all().first()
        response = self.client.get(f"/drone-delivery/drone/{drone.slug}/detail/")

        self.assertEqual(response.status_code, 200)
