from django.core.management.base import BaseCommand

from drone_delivery.models import (Drone)

class Command(BaseCommand):
    help = "Delete all Photos"

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
            '--all',
            action="store_true",
            help="Deleting all data"
        )

    def handle(self, *args, **options):
        if options["drones"] or options["all"]:
            drones = Drone.objects.all()            
            drones.delete()

        if options["medications"] or options["all"]:
            # todo
            pass

        self.stdout.write("SUCCESS")