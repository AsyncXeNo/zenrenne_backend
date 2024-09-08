from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from api.models import CarModel, Make, Product, ProductMakeModelConnection

class Command(BaseCommand):
    help = 'Create a product for each last-level submodel (or model if no submodel), and create corresponding ProductMakeModelConnection'

    def handle(self, *args, **kwargs):
        # Get all makes
        makes = Make.objects.all()

        for make in makes:
            # Get all models for this make
            models = CarModel.objects.filter(parent_type=ContentType.objects.get_for_model(Make), parent_id=make.id)

            for model in models:
                # Check if the model has any submodels
                submodels = CarModel.objects.filter(parent_type=ContentType.objects.get_for_model(CarModel), parent_id=model.id)

                if submodels.exists():
                    for submodel in submodels:
                        # Ensure the submodel does not have any further submodels under it
                        further_submodels = CarModel.objects.filter(parent_type=ContentType.objects.get_for_model(CarModel), parent_id=submodel.id)
                        if not further_submodels.exists():
                            # Create product for the last-level submodel
                            product_name = f"ZenRenne Autowerke ValveLogicTM Exhaust System - {make.name} {model.name} {submodel.name}"
                            product, created = Product.objects.get_or_create(name=product_name)

                            if created:
                                self.stdout.write(self.style.SUCCESS(f'Product created: {product_name}'))
                            else:
                                self.stdout.write(self.style.WARNING(f'Product already exists: {product_name}'))

                            # Create ProductMakeModelConnection for the product with Make, Model, and Submodel
                            self.create_product_make_model_connection(product, make, model, submodel)

                else:
                    # If the model has no submodels, create a product for the model itself
                    product_name = f"ZenRenne Autowerke ValveLogicTM Exhaust System - {make.name} {model.name}"
                    product, created = Product.objects.get_or_create(name=product_name)

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Product created: {product_name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Product already exists: {product_name}'))

                    # Create ProductMakeModelConnection for the product with Make and Model
                    self.create_product_make_model_connection(product, make, model)

        self.stdout.write(self.style.SUCCESS('Product creation and connection operation complete'))

    def create_product_make_model_connection(self, product, make, model, submodel=None):
        """
        Helper function to create ProductMakeModelConnection for the given product and make/model/submodel.
        """
        # Connect the product with the make
        make_content_type = ContentType.objects.get_for_model(Make)
        ProductMakeModelConnection.objects.get_or_create(
            product=product,
            parent_type=make_content_type,
            parent_id=make.id
        )

        # Connect the product with the model
        model_content_type = ContentType.objects.get_for_model(CarModel)
        ProductMakeModelConnection.objects.get_or_create(
            product=product,
            parent_type=model_content_type,
            parent_id=model.id
        )

        # If submodel exists, connect the product with the submodel
        if submodel:
            ProductMakeModelConnection.objects.get_or_create(
                product=product,
                parent_type=model_content_type,
                parent_id=submodel.id
            )
