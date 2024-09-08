from django.core.management.base import BaseCommand
from api.models import Product

class Command(BaseCommand):
    help = 'List all existing product names'

    def handle(self, *args, **kwargs):
        # Query all products
        products = Product.objects.all()

        # Print the name of each product
        if products.exists():
            for product in products:
                self.stdout.write(self.style.SUCCESS(f'Product: {product.name}'))
        else:
            self.stdout.write(self.style.WARNING('No products found.'))