from django.core.management.base import BaseCommand
from api.models import Product, Variant

class Command(BaseCommand):
    help = 'Create 4 variants for each product with specific names and product names'

    def handle(self, *args, **kwargs):
        # Define the variant details
        variant_details = [
            {
                'name': 'Catless Downpipe',
                'product_name': 'ZenRenne Autowerke Catless Downpipe with Heat Shield - {product_name}'
            },
            {
                'name': 'Catted Downpipe',
                'product_name': 'ZenRenne Autowerke Catted Downpipe with Heat Shield - {product_name}'
            },
            {
                'name': 'Stainless Steel Catback',
                'product_name': 'ZenRenne Autowerke ValveLogic T304 Stainless Steel Catback Exhaust System - {product_name}'
            },
            {
                'name': 'Titanium Catback',
                'product_name': 'ZenRenne Autowerke ValveLogic Grade5 Titanium Catback Exhaust System - {product_name}'
            }
        ]

        # Fetch all products
        products = Product.objects.all()

        if not products.exists():
            self.stdout.write(self.style.WARNING("No products found"))
            return

        self.stdout.write(self.style.SUCCESS("Creating variants for all products"))

        # Create variants for each product
        for product in products:
            for variant_detail in variant_details:
                variant_name = variant_detail['name']
                variant_product_name = variant_detail['product_name'].format(product_name=product.name)
                
                Variant.objects.create(
                    name=variant_name,
                    product=product,
                    product_name=variant_product_name
                )

                self.stdout.write(f"Created Variant: {variant_name} for Product: {product.name}")
