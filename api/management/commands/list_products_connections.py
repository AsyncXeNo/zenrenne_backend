from django.core.management.base import BaseCommand
from api.models import Product, ProductMakeModelConnection, CarModel
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'List all products and their connections'

    def handle(self, *args, **kwargs):
        # List all products
        products = Product.objects.all()
        if not products.exists():
            self.stdout.write(self.style.WARNING("No products found"))
        else:
            self.stdout.write(self.style.SUCCESS("Listing all products:"))
            for product in products:
                self.stdout.write(self.style.SUCCESS(f"Product: {product.name}"))

        # List all ProductMakeModelConnections
        connections = ProductMakeModelConnection.objects.all()
        if not connections.exists():
            self.stdout.write(self.style.WARNING("No ProductMakeModelConnections found"))
        else:
            self.stdout.write(self.style.SUCCESS("Listing all ProductMakeModelConnections:"))
            for connection in connections:
                parent_model = connection.parent_type.model_class()
                parent_instance = parent_model.objects.get(id=connection.parent_id)
                self.stdout.write(self.style.SUCCESS(f"Product: {connection.product.name} - Parent: {parent_instance.name}"))
