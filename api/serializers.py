from rest_framework import serializers
from .models import (
    Make, 
    CarModel, 
    Product, 
    ProductMakeModelConnection, 
    Variant, 
    VariantImage,
    Stat,
    AudioTrack,
    NewsletterSubscriber
)
from django.contrib.contenttypes.models import ContentType

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id', 'app_label', 'model']

class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id', 'name']

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'parent_type', 'parent_id']
        depth = 1  # Depth to automatically serialize related parent fields

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']

class ProductMakeModelConnectionSerializer(serializers.ModelSerializer):
    # parent_type = serializers.SlugRelatedField(slug_field='model', queryset=ContentType.objects.only('model'))

    class Meta:
        model = ProductMakeModelConnection
        fields = ['product', 'parent_type', 'parent_id']

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'name', 'product_name', 'description', 'product']
        depth = 1  # Automatically serialize related Product

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

        if not self.instance and variant.stats.count() >= 3:
            raise serializers.ValidationError("A variant can only have 3 stats.")

        if not self.instance and Stat.objects.filter(variant=variant, name=name).exists():
            raise serializers.ValidationError("Stat names must be unique within the same variant.")

        return data

class AudioTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioTrack
        fields = ['id', 'name', 'track', 'variant']

    def validate(self, data):
        variant = data['variant']
        name = data['name']

        if not self.instance and variant.audio_tracks.count() >= 3:
            raise serializers.ValidationError("A variant can only have 3 audio tracks.")

        if not self.instance and AudioTrack.objects.filter(variant=variant, name=name).exists():
            raise serializers.ValidationError("Audio track names must be unique within the same variant.")

        return data


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'subscribed_at', 'unsubscribed']