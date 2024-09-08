from rest_framework import serializers
from .models import (
    Make, 
    CarModel, 
    Product, 
    ProductMakeModelConnection, 
    Variant, 
    VariantImage,
    Stat,
    AudioTrack
)
from django.contrib.contenttypes.models import ContentType


class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id', 'name']


class ModelSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = CarModel
        fields = ['id', 'name', 'parent_type', 'parent_id', 'parent']

    def get_parent(self, obj):
        if obj.parent_type.model == 'make':
            # If parent_type is Make
            return MakeSerializer(Make.objects.get(id=obj.parent_id)).data
        elif obj.parent_type.model == 'carmodel':
            # If parent_type is CarModel
            return ModelSerializer(CarModel.objects.get(id=obj.parent_id)).data
        return None
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class ProductMakeModelConnectionSerializer(serializers.ModelSerializer):
    parent_type = serializers.SlugRelatedField(slug_field='model', queryset=ContentType.objects.all())
    parent = serializers.SerializerMethodField()

    class Meta:
        model = ProductMakeModelConnection
        fields = ['product', 'parent_type', 'parent']

    def get_parent(self, obj):
        return str(obj.parent)
    

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'name', 'product_name', 'description', 'product']


class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantImage
        fields = ['id', 'image', 'variant', 'is_main']

    
class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['id', 'name', 'number', 'unit', 'additional', 'variant']

    def validate(self, data):
        variant = data['variant']
        name = data['name']

        # Check the count of stats for the variant
        if variant.stats.count() >= 3 and not self.instance:
            raise serializers.ValidationError("A variant can only have 3 stats.")

        # Check for unique name within the same variant
        if Stat.objects.filter(variant=variant, name=name).exists() and not self.instance:
            raise serializers.ValidationError("Stat names must be unique within the same variant.")

        return data


class AudioTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioTrack
        fields = ['id', 'name', 'track', 'variant']

    def validate(self, data):
        variant = data['variant']
        name = data['name']

        # Check if the variant already has 3 audio tracks
        if variant.audio_tracks.count() >= 3 and not self.instance:
            raise serializers.ValidationError("A variant can only have 3 audio tracks.")

        # Check for unique name within the same variant
        if AudioTrack.objects.filter(variant=variant, name=name).exists() and not self.instance:
            raise serializers.ValidationError("Audio track names must be unique within the same variant.")

        return data