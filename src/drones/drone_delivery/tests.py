import random
from http import HTTPStatus
from django.test import TestCase

from .serializers import DroneSerializer

from .models import (Drone, Medication)
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

    def test_create_drone_rest_api(self):
        obj = self.random_data_generate()

        drone = DroneSerializer(data = obj)
        if drone.is_valid():
            drone.save()

        self.assertTrue(Drone.objects.filter(serial_number = obj["serial_number"]).exists())

    # def test_update_drone_rest_api(self):
    #     obj = self.random_data_generate()
        
    #     drone = DroneSerializer(data = obj)
    #     if drone.is_valid():
    #         drone.save()
        
    #     obj_drone = Drone.objects.filter(serial_number = obj["serial_number"]).first()
        
    #     # Modifying fields
    #     state = random.choice(tuple(filter(lambda x: x[0] != obj_drone.state, Drone.STATES)))
    #     update = {"battery_capacity": 90, "state": state}
    #     drone_update = DroneSerializer(obj_drone, data= update, partial=True)

    #     if drone_update.is_valid():
    #         drone_update.save()

    #     obj_update_drone = Drone.objects.filter(serial_number = obj_drone.serial_number).first()

    #     self.assertEqual(obj_drone.serial_number, obj_update_drone.serial_number)

    #     self.assertNotEqual(obj_drone.battery_capacity, obj_update_drone.battery_capacity)
    #     self.assertEqual(obj_update_drone.battery_capacity, update["battery_capacity"])

    #     self.assertNotEqual(obj_update_drone.state, obj_update_drone.state)
    #     self.assertEqual(obj_update_drone.state, update["state"])

    def test_api_drone_url(self):
        response = self.client.get("/drone-delivery/api/drone/list/")
        
        self.assertEqual(response.status_code, HTTPStatus.OK)


class MedicationTestCase(TestCase):
    def random_code_generate(self):
        allows_characteres = [chr(i) for i in range(65, 91)] + list(map(str, range(0, 10))) + ["_", "-"]
        L = len(allows_characteres)
        code = []
        code_len = random.randrange(10)
        while len(code) <= code_len:
            i = random.randrange(L)
            code.append(allows_characteres[i])        
        return "".join(code)

    def setUp(self):
        medications = ["Acetaminophen", "Adenosine", "Alprostadil", "Amiodarone", "Amitriptyline", "Ampicillin", "Anastrozole", "Apomorphine", "Ascorbic", "Atropine", "Baclofen", "Benzocaine", "Benzyl", "Betadine", "Solution", "Betamethasone", "Phosphate", "Biotin", "Bromfenac", "Brompheniramine", "Budesonide", "Bupivacaine", "Buprenorphine", "Caffeine"]

        for i in medications:
            obj = {
                "name": i,
                "weight": random.randrange(500),
                "code": self.random_code_generate(),
                "image": "medications/2022/01/11/example.jpg"
            }
            medication = Medication(**obj)
            medication.save()
    
    def test_create_medication(self):
        medication = Medication.objects.all()

        self.assertGreater(len(medication), 0)
        
    