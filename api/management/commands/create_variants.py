from django.core.management.base import BaseCommand
from api.models import Product, Variant

class Command(BaseCommand):
    help = 'Create 4 variants for each product.'

    def handle(self, *args, **kwargs):
        # Define the variant names and their corresponding product name templates
        variant_data = [
            ("Catless Downpipe", "ZenRenne Autowerke Catless Downpipe with Heat Shield - {}"),
            ("Catted Downpipe", "ZenRenne Autowerke Catted Downpipe with Heat Shield - {}"),
            ("Stainless Steel Catback", "ZenRenne Autowerke ValveLogic T304 Stainless Steel Catback Exhaust System - {}"),
            ("Titanium Catback", "ZenRenne Autowerke ValveLogic Grade5 Titanium Catback Exhaust System - {}"),
        ]

        # Fetch all products
        products = Product.objects.all()

        for product in products:
            self.stdout.write(self.style.SUCCESS(f"Processing product: {product.name}"))

            for variant_name, product_name_template in variant_data:
                product_name = product_name_template.format(product.name.split(' - ')[-1])  # Get the car/model part of the product name
                variant, created = Variant.objects.get_or_create(
                    name=variant_name,
                    product=product,
                    product_name=product_name,
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created variant: {variant_name} for product: {product.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Variant {variant_name} for product {product.name} already exists."))

        self.stdout.write(self.style.SUCCESS('Variants creation completed successfully.'))
