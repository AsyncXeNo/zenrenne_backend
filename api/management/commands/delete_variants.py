from django.core.management.base import BaseCommand
from api.models import Variant

class Command(BaseCommand):
    help = 'Delete all variants from the database'

    def handle(self, *args, **kwargs):
        # Fetch all variants
        variants = Variant.objects.all()

        if not variants.exists():
            self.stdout.write(self.style.WARNING("No variants found to delete"))
            return

        # Delete all variants
        count, _ = variants.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} variants"))
