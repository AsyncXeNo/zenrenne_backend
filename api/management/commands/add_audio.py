import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from api.models import Variant, AudioTrack
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create AudioTrack records for each variant based on the audio folders, with filename parsing for names'

    def handle(self, *args, **kwargs):
        # Path to the base directory where audio files are stored
        audio_base_path = os.path.join(settings.BASE_DIR, 'data', 'audio')

        # Load the Excel file (replace this with the actual path if necessary)
        excel_file_path = r'C:\Users\kavya\OneDrive\Desktop\Dev\zenrenne_backend\variant_image_folders.xlsx'

        import pandas as pd
        try:
            df = pd.read_excel(excel_file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading Excel file: {e}"))
            return

        # Iterate over the rows in the Excel file
        for _, row in df.iterrows():
            # Strip any extra spaces from the product_name
            product_name = row[0].strip()
            audio_folder = row[2]  # Third column for audio folder

            if pd.isna(audio_folder):
                self.stdout.write(self.style.WARNING(f"No audio folder found for product: {product_name}"))
                continue

            # Fetch the variant associated with this product_name
            try:
                variant = Variant.objects.get(product_name=product_name)
            except Variant.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Variant not found for product_name: {product_name}"))
                continue

            # Path to the audio folder for this variant
            variant_audio_folder_path = os.path.join(audio_base_path, audio_folder)

            if not os.path.exists(variant_audio_folder_path):
                self.stdout.write(self.style.ERROR(f"Audio folder not found: {variant_audio_folder_path}"))
                continue

            # List all .mp3 files in the folder
            audio_files = [f for f in sorted(os.listdir(variant_audio_folder_path)) if f.endswith('.mp3')]

            if not audio_files:
                self.stdout.write(self.style.WARNING(f"No audio files found in folder: {variant_audio_folder_path}"))
                continue

            # Create AudioTrack records for the variant
            for audio_file in audio_files:
                audio_path = os.path.join(variant_audio_folder_path, audio_file)
                
                # Derive the name from the filename (without extension), replace underscores with spaces, and capitalize
                name = os.path.splitext(audio_file)[0].replace('_', ' ').title()

                with open(audio_path, 'rb') as audio_file_obj:
                    audio_track = AudioTrack(
                        variant=variant,
                        name=name,
                        track=File(audio_file_obj, name=audio_file)
                    )
                    audio_track.save()

                    self.stdout.write(self.style.SUCCESS(f"Added audio track '{name}' for variant: {variant.product_name}"))

            logger.info(f"Processed audio tracks for variant: {variant.product_name}")