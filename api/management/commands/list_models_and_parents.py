from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from api.models import CarModel

class Command(BaseCommand):
    help = 'List all car models and their parents'

    def handle(self, *args, **kwargs):
        # Fetch all car models
        car_models = CarModel.objects.all()

        if not car_models.exists():
            self.stdout.write(self.style.WARNING("No car models found"))
            return

        # List all models and their parents
        self.stdout.write(self.style.SUCCESS("Listing all car models and their parents:"))
        for car_model in car_models:
            parent_model = car_model.parent_type.model_class()  # Get the parent model class
            parent_instance = parent_model.objects.get(id=car_model.parent_id)  # Get the parent instance
            self.stdout.write(f"Car Model: {car_model.name} - Parent: {parent_instance}")
