import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from api.models import Variant, VariantImage
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create VariantImage records for each variant based on the image folders, skip if images already exist'

    def handle(self, *args, **kwargs):
        # Path to the base directory where images are stored
        images_base_path = os.path.join(settings.BASE_DIR, 'data', 'images')

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
            image_folder = row[1].strip()

            if pd.isna(image_folder):
                self.stdout.write(self.style.WARNING(f"No image folder found for product: {product_name}"))
                continue

            # Fetch the variant associated with this product_name
            try:
                variant = Variant.objects.get(product_name=product_name)
            except Variant.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Variant not found for product_name: {product_name}"))
                continue

            # Check if the variant already has images
            if variant.images.exists():
                self.stdout.write(self.style.WARNING(f"Variant '{product_name}' already has images, skipping."))
                continue

            # Path to the image folder for this variant
            variant_image_folder_path = os.path.join(images_base_path, image_folder)

            if not os.path.exists(variant_image_folder_path):
                self.stdout.write(self.style.ERROR(f"Image folder not found: {variant_image_folder_path}"))
                continue

            # List all .jpg files in the folder
            image_files = [f for f in sorted(os.listdir(variant_image_folder_path)) if f.endswith('.jpg')]

            if not image_files:
                self.stdout.write(self.style.WARNING(f"No image files found in folder: {variant_image_folder_path}"))
                continue

            # Create VariantImage records for the variant
            for index, image_file in enumerate(image_files):
                image_path = os.path.join(variant_image_folder_path, image_file)
                is_main = index == 0  # The first image will be set as the main image

                with open(image_path, 'rb') as img_file:
                    variant_image = VariantImage(
                        variant=variant,
                        image=File(img_file, name=image_file),
                        is_main=is_main
                    )
                    variant_image.save()

                    if is_main:
                        self.stdout.write(self.style.SUCCESS(f"Main image set for variant: {variant.product_name}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Added image for variant: {variant.product_name}"))

            logger.info(f"Processed images for variant: {variant.product_name}")
