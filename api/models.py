import os
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage


class Make(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Make"
        verbose_name_plural = "Makes"


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
        unique_together = ('name', 'parent_type', 'parent_id')
        indexes = [models.Index(fields=['parent_id', 'parent_type'])]  # Add index


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProductMakeModelConnection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    parent_id = models.PositiveIntegerField()
    parent = GenericForeignKey('parent_type', 'parent_id')

    def __str__(self):
        return f"Product {self.product.id} -> {self.parent}"

    class Meta:
        unique_together = ('product', 'parent_type', 'parent_id')
        indexes = [models.Index(fields=['parent_id', 'parent_type'])]  # Add index


class Variant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=200)
    description = models.TextField(max_length=3000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')

    def __str__(self):
        return self.name


class VariantImage(models.Model):
    image = models.ImageField(upload_to='variant_images/')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='images')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.variant.name}"
    
    def save(self, *args, **kwargs):
        if self.is_main:
            # Set other images of the same variant to not be the main image
            VariantImage.objects.filter(variant=self.variant, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)


@receiver(post_delete, sender=VariantImage)
def delete_variant_image_file(sender, instance, **kwargs):
    if instance.image:
        default_storage.delete(instance.image.name)


class Stat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12)
    number = models.CharField(max_length=12)
    unit = models.CharField(max_length=12)
    additional = models.CharField(max_length=20, blank=True, null=True)
    variant = models.ForeignKey('Variant', on_delete=models.CASCADE, related_name='stats')

    def __str__(self):
        return f"Stat for {self.variant}, {self.name}"

    def save(self, *args, **kwargs):
        if self.variant.stats.count() >= 3:
            raise ValueError("A variant can only have 3 stats.")
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['variant', 'name'], name='unique_stat_name_per_variant')
        ]


class AudioTrack(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    track = models.FileField(upload_to='audio_tracks/')
    variant = models.ForeignKey('Variant', on_delete=models.CASCADE, related_name='audio_tracks')

    def __str__(self):
        return f"Audio Track for {self.variant}, {self.name}"

    def save(self, *args, **kwargs):
        if self.variant.audio_tracks.count() >= 3 and not self.pk:
            raise ValueError("A variant can only have 3 audio tracks.")
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['variant', 'name'], name='unique_audio_track_name_per_variant')
        ]


@receiver(post_delete, sender=AudioTrack)
def delete_audio_file(sender, instance, **kwargs):
    if instance.track:
        default_storage.delete(instance.track.name)


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.email