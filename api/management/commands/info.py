from django.core.management.base import BaseCommand
from api.models import Variant

class Command(BaseCommand):
    help = 'Display the number of variants with images and audio tracks associated with them'

    def handle(self, *args, **kwargs):
        # Count variants that have at least one associated image
        variants_with_images_count = Variant.objects.filter(images__isnull=False).distinct().count()

        # Count variants that have at least one associated audio track
        variants_with_audio_tracks_count = Variant.objects.filter(audio_tracks__isnull=False).distinct().count()

        # Output the counts
        self.stdout.write(self.style.SUCCESS(f"Number of variants with images: {variants_with_images_count}"))
        self.stdout.write(self.style.SUCCESS(f"Number of variants with audio tracks: {variants_with_audio_tracks_count}"))
