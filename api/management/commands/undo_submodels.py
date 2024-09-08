from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from api.models import CarModel

# Data that was previously added
DATA = [
    ("Alfa Romeos", "Giulia Quadrifoglio", "NA"),
    ("Audi", "RS3", "8V"),
    ("Audi", "S3", "8V"),
    ("Audi", "A3", "8V"),
    ("Audi", "TT / TT-S", "8V"),
    ("BMW", "1 Series M", "E82"),
    ("BMW", "120i / 128i / 228i / 320i / 328i / 428i", "F20 / F21 / F22 / F30 / F32 / F33 / F36"),
    ("BMW", "340i / 440i", "F30 / F31 / F32 / F33 / F34 / F36"),
    ("BMW", "540i / 640i", "G30 / G31 / G32"),
    ("BMW", "M135i / M235i", "F20 / F22"),
    ("BMW", "M140i / M240i", "F20 / F22"),
    ("BMW", "M140i / M240i", "G40 / G42"),
    ("BMW", "M340i / M440i", "G20 / G21 / G22 / G23 / G26"),
    ("BMW", "M2", "F87"),
    ("BMW", "M2 Competition", "F87"),
    ("BMW", "M3", "E90 / E92 / E93"),
    ("BMW", "M3 / M4", "F80 / F82 / F83"),
    ("BMW", "M3 / M4", "G80 / G82 / G83"),
    ("BMW", "M5", "F10"),
    ("BMW", "M5", "F90"),
    ("BMW", "X3 M40i / X4 M40i", "G01 / G02"),
    ("BMW", "X3M / X4M", "F97 / F98"),
    ("BMW", "X5M / X6M", "F85 / F86"),
    ("BMW", "X5M / X6M", "F95 / F96"),
    ("Ferrari", "458 Italia", "NA"),
    ("Ferrari", "812 Superfast", "NA"),
    ("Ferrari", "F12berlinetta", "NA"),
    ("Ferrari", "F8 Tributo", "NA"),
    ("Ferrari", "FF", "NA"),
    ("Nissan", "R35 GTR", "NA"),
    ("Porsche", "911 Carrera", "NA"),
    ("Porsche", "911 Turbo", "NA"),
    ("Porsche", "Cayenne", "9Y0 (2019+)"),
    ("Porsche", "Cayenne", "958.2 (2015-2018)"),
    ("Porsche", "Cayenne", "958.1 (2011-2014)"),
    ("Porsche", "Boxster / Cayman", "718 GT4 / GTS / SPYDER (2020+)"),
    ("Porsche", "Boxster / Cayman", "718 (2017+)"),
    ("Porsche", "Boxster / Cayman", "981 (2013-2016)"),
    ("Porsche", "Boxster / Cayman", "981 GT4 / SPYDER / CLUBSPORT (2015-2016)"),
    ("Porsche", "Boxster / Cayman", "987.2 (2009-2012)"),
    ("Porsche", "Boxster / Cayman", "987.1 (2005-2008)"),
    ("Porsche", "Boxster / Cayman", "986 (1997-2004)"),
    ("Porsche", "Macan", "95B S / GTS / Turbo (2014+)"),
    ("Porsche", "Macan", "2.0T (2016+)"),
    ("Porsche", "Macan", "2.9T S / GTS (2022+)"),
    ("Toyota", "Supra", "A90"),
    ("Honda", "Civic Type R", "FL5"),
    ("VW", "Golf R", "MK7 / MK7.5"),
    ("VW", "Golf GTi", "MK7 / MK7.5"),
    ("VW", "Golf GTi", "MK8"),
]

class Command(BaseCommand):
    help = 'Undo the addition of submodels (delete them from the database)'

    def handle(self, *args, **kwargs):
        for make_name, model_name, submodel_name in DATA:
            if submodel_name == "NA":
                continue  # Skip records with submodel "NA"
            
            try:
                # Find the parent model
                parent_model = CarModel.objects.get(name=model_name)

                # Delete submodels (children of the model)
                submodels = submodel_name.split(" / ")
                for submodel in submodels:
                    deleted, _ = CarModel.objects.filter(
                        name=submodel,
                        parent_type=ContentType.objects.get_for_model(CarModel),
                        parent_id=parent_model.id
                    ).delete()
                    if deleted:
                        self.stdout.write(self.style.SUCCESS(f'Deleted submodel {submodel} under parent {model_name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'No submodel {submodel} found under parent {model_name}'))

            except CarModel.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Model {model_name} not found in the database'))

        self.stdout.write(self.style.SUCCESS('Undo submodel operation complete'))
