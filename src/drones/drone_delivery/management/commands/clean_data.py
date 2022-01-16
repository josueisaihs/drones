from django.core.management.base import BaseCommand

from drone_delivery.models import (
    Drone, 
    Medication, 
    DeliveryPackage,
    Package
)

class Command(BaseCommand):
    help = "Delete Drone, Medication, Package and Delivery model"

    def add_arguments(self, parser):
        parser.add_argument(
            '--drones',
            action="store_true",
            help="Deleting drones data"
        )

        parser.add_argument(
            '--medications',
            action="store_true",
            help="Create the medication data"
        )

        parser.add_argument(
            '--delivery',
            action="store_true",
            help="Create the delivery data"
        )

        parser.add_argument(
            '--package',
            action="store_true",
            help="Create the package data"
        )

        parser.add_argument(
            '--all',
            action="store_true",
            help="Deleting all data"
        )

    def handle(self, *args, **options):
        if options["package"] or options["all"]:
            packages = Package.objects.all()
            self.stdout.write(f"DELETING {len(packages)} packages...")  
            packages.delete()

        if options["delivery"] or options["all"]:
            deliveries = DeliveryPackage.objects.all()
            self.stdout.write(f"DELETING {len(deliveries)} deliveries...")  
            deliveries.delete()

        if options["drones"] or options["all"]:
            drones = Drone.objects.all() 
            self.stdout.write(f"DELETING {len(drones)} drones...")           
            drones.delete()

        if options["medications"] or options["all"]:
            medications = Medication.objects.all()
            self.stdout.write(f"DELETING {len(medications)} medications...")  
            medications.delete()        

        self.stdout.write("SUCCESS")