from django.core.management.base import BaseCommand
from api.models import AudioTrack

class Command(BaseCommand):
    help = 'Delete all AudioTrack records from the database'

    def handle(self, *args, **kwargs):
        # Fetch all AudioTrack records
        audio_tracks = AudioTrack.objects.all()

        if not audio_tracks.exists():
            self.stdout.write(self.style.WARNING("No AudioTrack records found to delete"))
            return

        # Delete all AudioTrack records
        count, _ = audio_tracks.delete()

        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} AudioTrack records"))
