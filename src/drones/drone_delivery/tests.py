import random
from http import HTTPStatus

from django.db import IntegrityError
from django.test import TestCase

from .models import (Drone)
from .forms import (DroneForm)

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
            drone = Drone(**obj)
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

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_drone_form(self):
        obj = self.random_data_generate()
        drone = DroneForm(data = obj)

        if drone.is_valid():
            drone.save()

            self.assertTrue(drone.is_valid())
            self.assertTrue(Drone.objects.filter(serial_number = obj["serial_number"]).exists())

    def test_drone_form_error_messages(self):
        obj = self.random_data_generate()
        obj["battery_capacity"] = random.randint(a = 101, b = 150)
        obj["weight_limit"] = 601

        drone = DroneForm(data = obj)

        error_battery = ['<ul class="errorlist"><li>The value %s for the Battery Capacity is wrong. Battery Capacity must be value between 0 and 100</li></ul>' % obj["battery_capacity"]]
        error_weight = ['<ul class="errorlist"><li>The value %s as Weight Limit is wrong. The value must be a maximum of 500g.</li></ul>' % obj["weight_limit"]]

        self.assertFalse(drone.is_valid())
        self.assertEqual(drone.errors["battery_capacity"], error_battery)
        self.assertEqual(drone.errors["weight_limit"], error_weight) 

