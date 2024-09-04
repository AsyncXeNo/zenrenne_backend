import os
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
class Make(models.Model):
    icon = models.FileField(upload_to='icons/')
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Make"
        verbose_name_plural = "Makes"
    

@receiver(post_delete, sender=Make)
def delete_make_icon_file(sender, instance, **kwargs):
    if instance.icon and os.path.isfile(instance.icon.path):
        os.remove(instance.icon.path)


class CarModel(models.Model):
    name = models.CharField(max_length=50)
    
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    parent_id = models.PositiveIntegerField()
    parent = GenericForeignKey('parent_type', 'parent_id')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class ProductMakeModelConnection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    parent_id = models.PositiveIntegerField()
    parent = GenericForeignKey('parent_type', 'parent_id')

    class Meta:
        unique_together = ('product', 'parent_type', 'parent_id')

    def __str__(self):
        return f"Product {self.product.id} -> {self.parent}"
    

class Variant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=3000)  # Store description as plain text
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')

    def __str__(self):
        return self.name
    

class VariantImage(models.Model):
    image = models.ImageField(upload_to='variant_images/')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for {self.variant.name}"


@receiver(post_delete, sender=VariantImage)
def delete_variant_image_file(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


class Stat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12)
    number = models.CharField(max_length=12)
    unit = models.CharField(max_length=12)
    additional = models.CharField(max_length=20, blank=True, null=True)
    variant = models.ForeignKey('Variant', on_delete=models.CASCADE, related_name='stats')

    def __str__(self):
        return f"Stat for {self.variant}, {self.name}"
    


class AudioTrack(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    track = models.FileField(upload_to='audio_tracks/')
    variant = models.ForeignKey('Variant', on_delete=models.CASCADE, related_name='audio_tracks')

    def __str__(self):
        return f"Audio Track for {self.variant}, {self.name}"
    

@receiver(post_delete, sender=AudioTrack)
def delete_audio_file(sender, instance, **kwargs):
    if instance.track and os.path.isfile(instance.track.path):
        os.remove(instance.track.path)