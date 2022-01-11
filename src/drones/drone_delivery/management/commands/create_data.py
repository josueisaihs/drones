from django.core.management.base import BaseCommand

from drone_delivery.models import Drone
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

    def handle(self, *args, **options):
        if options["drones"] or options["all"]: self.creating_drone_data()
        if options["medications"] or options["all"]: 
            # todo
            pass

        self.stdout.write("SUCCESS")