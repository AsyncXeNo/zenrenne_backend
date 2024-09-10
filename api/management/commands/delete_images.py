from django.core.management.base import BaseCommand
from api.models import VariantImage

class Command(BaseCommand):
    help = 'Delete all VariantImage records from the database'

    def handle(self, *args, **kwargs):
        # Fetch all VariantImage records
        variant_images = VariantImage.objects.all()

        if not variant_images.exists():
            self.stdout.write(self.style.WARNING("No VariantImage records found to delete"))
            return

        # Delete all VariantImage records
        count, _ = variant_images.delete()

        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} VariantImage records"))
