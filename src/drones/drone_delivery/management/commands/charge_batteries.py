from random import randrange

from django.core.management.base import BaseCommand

from drone_delivery.models import Drone

class Command(BaseCommand):
    help = "Reset Battery State of Charge"

    def add_arguments(self, parser):
        parser.add_argument(
            '--random',
            action="store_true",
            help="Create the drone data"
        )
    
    def handle(self, *args, **options):
        for drone in Drone.objects.all():
            drone.battery_capacity = randrange(10, 100) if options["random"] else 100
            drone.save()
            self.stdout.write(f"Drone: {drone.serial_number}, Battery {drone.battery_capacity}%") 
        self.stdout.write("SUCCESS!")