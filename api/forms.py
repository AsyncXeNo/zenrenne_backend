# api/forms.py

from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import (
    Make, 
    CarModel, 
    ProductMakeModelConnection, 
    Variant, 
    Product, 
    VariantImage,
    Stat,
    AudioTrack
)


class VariantForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Product"
    )

    class Meta:
        model = Variant
        fields = ['name', 'description', 'product']


class CarModelForm(forms.ModelForm):
    current_parent = forms.CharField(
        label="Current Parent (readonly)",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    make_parent = forms.ModelChoiceField(
        queryset=Make.objects.all(),
        required=False,
        label="Parent Make",
    )
    model_parent = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        required=False,
        label="Parent Model",
    )

    class Meta:
        model = CarModel
        fields = ['name', 'current_parent', 'make_parent', 'model_parent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate the current_parent field with the existing parent information
        if self.instance and self.instance.pk:
            parent = self.instance.parent
            if parent:
                self.fields['current_parent'].initial = f"{parent} ({self.instance.parent_type})"

    def clean(self):
        cleaned_data = super().clean()
        make = cleaned_data.get('make_parent')
        model = cleaned_data.get('model_parent')

        # Ensure that only one of make_parent or model_parent is selected
        if make and model:
            self.add_error(None, "Please select either a Make or a Model, not both.")
        elif not make and not model:
            self.add_error(None, "Please select either a Make or a Model.")

        # Check if the selected parent is the instance itself
        if model and model.id == self.instance.id:
            self.add_error('model_parent', "A model cannot be its own parent.")
        elif make and make.id == self.instance.id:
            self.add_error('make_parent', "A model cannot be its own parent.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        make = self.cleaned_data.get('make_parent')
        model = self.cleaned_data.get('model_parent')

        if make:
            instance.parent_type = ContentType.objects.get_for_model(make)
            instance.parent_id = make.id
        elif model:
            instance.parent_type = ContentType.objects.get_for_model(model)
            instance.parent_id = model.id

        if commit:
            instance.save()
        return instance
    

class ProductMakeModelConnectionForm(forms.ModelForm):
    make_parent = forms.ModelChoiceField(
        queryset=Make.objects.all(),
        required=False,
        label="Parent Make",
    )
    model_parent = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        required=False,
        label="Parent Model",
    )

    class Meta:
        model = ProductMakeModelConnection
        fields = ['product', 'make_parent', 'model_parent']

    def clean(self):
        cleaned_data = super().clean()
        make = cleaned_data.get('make_parent')
        model = cleaned_data.get('model_parent')

        # Ensure that only one of make_parent or model_parent is selected
        if make and model:
            self.add_error(None, "Please select either a Make or a Model, not both.")
        elif not make and not model:
            self.add_error(None, "Please select either a Make or a Model.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        make = self.cleaned_data.get('make_parent')
        model = self.cleaned_data.get('model_parent')

        if make:
            instance.parent_type = ContentType.objects.get_for_model(make)
            instance.parent_id = make.id
        elif model:
            instance.parent_type = ContentType.objects.get_for_model(model)
            instance.parent_id = model.id

        if commit:
            instance.save()
        return instance
    

class VariantImageAdminForm(forms.ModelForm):
    variant = forms.ModelChoiceField(
        queryset=Variant.objects.all(),  # Show all variants
        required=True,
        label="Variant"
    )
    
    class Meta:
        model = VariantImage
        fields = ['image', 'variant']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure that 'variant' queryset is populated with all available variants
        self.fields['variant'].queryset = Variant.objects.all()


class StatForm(forms.ModelForm):
    variant = forms.ModelChoiceField(
        queryset=Variant.objects.all(),
        required=True,
        label="Variant"
    )

    class Meta:
        model = Stat
        fields = ['name', 'number', 'unit', 'additional', 'variant']


class AudioTrackForm(forms.ModelForm):
    variant = forms.ModelChoiceField(
        queryset=Variant.objects.all(),
        required=True,
        label="Variant"
    )

    class Meta:
        model = AudioTrack
        fields = ['name', 'track', 'variant']