from django.core.management.base import BaseCommand
from api.models import Variant

class Command(BaseCommand):
    help = 'List all variants and display their product_name attributes'

    def handle(self, *args, **kwargs):
        # Fetch all variants
        variants = Variant.objects.all()

        if not variants.exists():
            self.stdout.write(self.style.WARNING("No variants found"))
            return

        self.stdout.write(self.style.SUCCESS("Listing all variants with their product names:"))

        # List all variants and their product names
        for variant in variants:
            self.stdout.write(f"{variant.product_name}")
