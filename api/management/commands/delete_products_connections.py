# your_app/management/commands/delete_all_products_and_connections.py

from django.core.management.base import BaseCommand
from api.models import Product, ProductMakeModelConnection

class Command(BaseCommand):
    help = 'Delete all Products and their associated ProductMakeModelConnections'

    def handle(self, *args, **kwargs):
        # Get all ProductMakeModelConnections
        connections = ProductMakeModelConnection.objects.all()
        num_connections = connections.count()

        if num_connections > 0:
            # Delete all ProductMakeModelConnections
            connections.delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {num_connections} ProductMakeModelConnections"))
        else:
            self.stdout.write(self.style.WARNING("No ProductMakeModelConnections found"))

        # Get all Products
        products = Product.objects.all()
        num_products = products.count()

        if num_products > 0:
            # Delete all Products
            products.delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {num_products} Products"))
        else:
            self.stdout.write(self.style.WARNING("No Products found"))
