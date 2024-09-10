from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from api.models import CarModel, Product, ProductMakeModelConnection, Make

class Command(BaseCommand):
    help = 'Create products for each last-level CarModel and add ProductMakeModelConnections'

    def handle(self, *args, **kwargs):
        # Get all CarModels that are not parents of any other models
        all_car_models = CarModel.objects.all()
        last_level_models = [
            car_model for car_model in all_car_models
            if not CarModel.objects.filter(parent_type=ContentType.objects.get_for_model(CarModel), parent_id=car_model.id).exists()
        ]

        self.stdout.write(self.style.SUCCESS(f"Found {len(last_level_models)} last-level models."))

        for car_model in last_level_models:
            try:
                # Construct the product name
                product_name = self.get_product_name(car_model)

                # Create a Product
                product = Product.objects.create(name=product_name)
                self.stdout.write(self.style.SUCCESS(f"Created Product: {product_name}"))

                # Create ProductMakeModelConnections
                self.create_connections(product, car_model)
                self.stdout.write(self.style.SUCCESS(f"Created ProductMakeModelConnections for Product: {product_name}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing CarModel {car_model.id}: {str(e)}"))

    def get_product_name(self, car_model):
        # Build the product name
        name_parts = []

        # Add the make and models from bottom to top
        current_model = car_model
        while current_model:
            name_parts.append(current_model.name)
            if isinstance(current_model, CarModel) and current_model.parent_type:
                parent_model = current_model.parent_type.model_class()
                if parent_model:
                    try:
                        current_model = parent_model.objects.get(id=current_model.parent_id)
                    except parent_model.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Parent CarModel not found: ID={current_model.parent_id}, Type={parent_model}"))
                        break
                else:
                    break
            elif isinstance(current_model, Make):
                break
            else:
                break

        make = name_parts.pop()
        return make + ' ' + ' '.join(name_parts)

    def create_connections(self, product, car_model):
        # Create ProductMakeModelConnections up the hierarchy
        current_model = car_model
        while current_model:
            try:
                ProductMakeModelConnection.objects.create(
                    product=product,
                    parent_type=ContentType.objects.get_for_model(current_model),
                    parent_id=current_model.id
                )
                if isinstance(current_model, Make):
                    break
                else:
                    parent_model = current_model.parent_type.model_class()
                    current_model = parent_model.objects.get(id=current_model.parent_id)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating connection for Product: {product.name}, CarModel ID={current_model.id}: {str(e)}"))
                break
