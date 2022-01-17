from random import randrange

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from drone_delivery.models import (
    Drone, 
    Medication, 
    Package
)
from drone_delivery.tests import DroneTestCase

class Command(BaseCommand):
    help = "Create the necessary data in the database to test the application"

    def add_arguments(self, parser):
        parser.add_argument(
            '--drones',
            action="store_true",
            help="Create the drone data"
        )

        parser.add_argument(
            '--medications',
            action="store_true",
            help="Create the medication data"
        )

        parser.add_argument(
            '--package',
            action="store_true",
            help="Create the delivery package data"
        )

        parser.add_argument(
            '--user',
            action="store_true",
            help="Create an user"
        )

        parser.add_argument(
            '--all',
            action="store_true",
            help="Create the drone & medication data"
        )

    def creating_drone_data(self):
        # Creating the Drone Data
        _t = DroneTestCase()
        for i in range(10):
            obj = _t.random_data_generate()

            while Drone.objects.filter(serial_number = obj["serial_number"]).exists():
                obj = _t.random_data_generate()
            drone = Drone(**obj)
            drone.save()

    def random_code_generate(self):
        """ Generate Code for Medication"""
        allows_characteres = [chr(i) for i in range(65, 91)] + list(map(str, range(0, 10))) + ["_",]
        L = len(allows_characteres)
        code = []
        code_len = randrange(10)
        while len(code) <= code_len:
            i = randrange(L)
            code.append(allows_characteres[i])        
        return "".join(code)

    def creating_medication_data(self):        
        medications = ["Acetaminophen", "Adenosine", "Alprostadil", "Amiodarone", "Amitriptyline", "Ampicillin", "Anastrozole", "Apomorphine", "Ascorbic", "Atropine", "Baclofen", "Benzocaine", "Benzyl", "Betadine", "Solution", "Betamethasone", "Phosphate", "Biotin", "Bromfenac", "Brompheniramine", "Budesonide", "Bupivacaine", "Buprenorphine", "Caffeine"]

        for i in medications:
            obj = {
                "name": i,
                "weight": randrange(1, 10),
                "code": self.random_code_generate(),
                "image": "medications/2022/01/11/example.jpg"
            }
            medication = Medication(**obj)
            medication.save()

    def creating_package_data(self):
        for i in range(10):
            package = Package()
            medication = Medication.objects.all().order_by("?").first()
            package.medication = Medication.objects.all().order_by("?").first()
            weight = 1000
            qty = randrange(1, 50)
            while weight >= 500: 
                qty = qty - 1          
                weight = medication.weight * qty
            package.qty = qty 
            package.save()

    def create_user(self):
        User = get_user_model()
        User.objects.filter(username = "admin").delete()
        
        user = User(username = "admin", email = "admin@example.com")
        user.is_staff = True
        user.is_superuser = True
        user.set_password("password")
        user.save()
            
    def handle(self, *args, **options):
        if options["drones"] or options["all"]: 
            self.creating_drone_data()
            self.stdout.write("Drones created :)")

        if options["medications"] or options["all"]: 
            self.creating_medication_data()
            self.stdout.write("Medications created :)")

        if options["package"] or options["all"]: 
            self.creating_package_data()
            self.stdout.write("Packages created :)")

        if options["user"] or options["all"]:
            self.create_user()
            self.stdout.write("User created :)")

        self.stdout.write("SUCCESS")