import random, json
from http import HTTPStatus, client
from tempfile import NamedTemporaryFile
from PIL import Image

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from .serializers import DroneSerializer

from .models import (
    Drone, 
    Medication,
    Package
)
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


class IntegrationTestCase(TestCase):
    username = "admin"
    password = ".@dm1n."

    def setUp(self):
        User = get_user_model()
        user = User(username = self.username, email = "admin@example.com")
        user.is_staff = True
        user.is_superuser = True
        user.set_password(self.password)
        user.save()

        medication_obj = {"name": "Acetaminophen", "weight": 10.0, "code": "ACET400",
                "image": "medications/2022/01/11/example.jpg"}
        medication = Medication(**medication_obj)
        medication.save()

        drone_obj =  {
            "serial_number": "45634564722",
            "model": "Cruiserweight", 
            "weight_limit": 400.0, 
            "battery_capacity": 98, 
            "state": "IDLE"
        }
        drone = Drone(**drone_obj)
        drone.save()

        package_obj = {
                "medication": medication,
                "qty": 5
        }
        package = Package(**package_obj)
        package.save()

    def test_drone_get(self):
        client = Client()
        response = client.get(reverse('drone_delivery:api-drone-list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_drone_post(self):
        client = Client()
        client.login(username = self.username, password = self.password)
        response = client.post(
            reverse('drone_delivery:api-drone-list'), 
            {
                "serial_number": "456345647", 
                "model": "Cruiserweight", 
                "weight_limit": 400.0, 
                "battery_capacity": 98, 
                "state": "IDLE"
            }, 
            content_type="application/json"
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
    
    def test_medication_get(self):
        client = Client()
        response = client.get(reverse('drone_delivery:api-medication-list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_drone_post(self):
        client = Client()
        client.login(username = self.username, password = self.password)
        image = Image.new("RGB", (100, 100))
        tmp_file = NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file)
        tmp_file.seek(0)
            
        obj = {
            "name": "Some_medicine",
            "weight": 400.0,
            "code": "SOM_400",
            "image": tmp_file
        }
        response = client.post(
            reverse('drone_delivery:api-medication-list'),
            data=obj,
            format='multipart'
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
    
    def test_package_get(self):
        client = Client()
        response = client.get(reverse('drone_delivery:api-package-list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_package_post(self):
        client = Client()
        client.login(username = self.username, password = self.password)

        pk = Medication.objects.get(name = "Acetaminophen").pk
        response = client.post(
            reverse('drone_delivery:api-package-list'), 
            {
                "medication": pk,
                "qty": 1
            }, 
            content_type="application/json"
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_delivery_get(self):
        client = Client()
        response = client.get(reverse('drone_delivery:api-delivery-list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delivery_post(self):
        client = Client()
        client.login(username = self.username, password = self.password)
        drone_pk = Drone.objects.all().first().pk
        package_pk = Package.objects.all().first().pk
        response = client.post(
            reverse('drone_delivery:api-delivery-list'),
            {
                "drone": drone_pk,
                "package": [package_pk,]
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
    