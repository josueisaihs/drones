from random import randrange

from django.core.management.base import BaseCommand

from drone_delivery.models import Drone, Medication, DeliveryPackage
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
            '--delivery',
            action="store_true",
            help="Create the delivery package data"
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
        allows_characteres = [chr(i) for i in range(65, 91)] + list(map(str, range(0, 10))) + ["_", "-"]
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
                "weight": randrange(500),
                "code": self.random_code_generate(),
                "image": "medications/2022/01/11/example.jpg"
            }
            medication = Medication(**obj)
            medication.save()

    def creating_delivery_data(self):
        for i in range(10):
            deliveryPackage = DeliveryPackage()
            deliveryPackage.drone = Drone.objects.all().order_by("?").first()
            deliveryPackage.medications.set([medication for medication in Medication.objects.all().order_by("?")[:1 + randrange(5)]])
            deliveryPackage.save()

            
    def handle(self, *args, **options):
        if options["drones"] or options["all"]: self.creating_drone_data()
        if options["medications"] or options["all"]: self.creating_medication_data()
        if options["delivery"] or options["all"]: self.creating_delivery_data()

        self.stdout.write("SUCCESS")