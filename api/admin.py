from django.contrib import admin
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
from .forms import (
    CarModelForm, 
    ProductMakeModelConnectionForm, 
    VariantForm, 
    VariantImageAdminForm,
    StatForm,
    AudioTrackForm
)
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(CarModel)
class ModelAdmin(admin.ModelAdmin):
    form = CarModelForm
    list_display = ('name', 'parent')
    list_display_links = ('name', 'parent')  # Make 'name' clickable to open the detailed view

    fieldsets = (
        (None, {
            'fields': ('name', 'current_parent')
        }),
        ('Parent Selection', {
            'fields': ('make_parent', 'model_parent'),
            'description': "Select either a Make or a Model as the parent. You cannot select both."
        }),
    )

    def parent(self, obj):
        parent = obj.parent
        if parent:
            parent_type = obj.parent_type.model
            parent_id = obj.parent_id

            if parent_type == 'make':
                parent_admin_url = reverse(f'admin:api_make_change', args=[parent_id])
            elif parent_type == 'carmodel':
                parent_admin_url = reverse(f'admin:api_carmodel_change', args=[parent_id])

            return format_html(f'<a href="{parent_admin_url}">{parent}</a>')
        return '-'
    parent.short_description = 'Parent'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(ProductMakeModelConnection)
class ProductMakeModelConnectionAdmin(admin.ModelAdmin):
    form = ProductMakeModelConnectionForm
    list_display = ('id', 'product_link', 'parent')
    list_display_links = ('id', 'product_link', 'parent')
    list_filter = ('parent_type',)

    fieldsets = (
        (None, {
            'fields': ('product',)  # Product field can be listed here if you need to show it in the main section
        }),
        ('Parent Selection', {
            'fields': ('make_parent', 'model_parent'),
            'description': "Select either a Make or a Model as the parent. You cannot select both.",
        }),
    )

    def parent(self, obj):
        parent = obj.parent
        if parent:
            parent_type = obj.parent_type.model
            parent_id = obj.parent_id

            if parent_type == 'make':
                parent_admin_url = reverse(f'admin:api_make_change', args=[parent_id])
            elif parent_type == 'carmodel':
                parent_admin_url = reverse(f'admin:api_carmodel_change', args=[parent_id])

            return format_html(f'<a href="{parent_admin_url}">{parent}</a>')
        return '-'
    
    parent.short_description = 'Parent'

    def product_link(self, obj):
        if obj.product:
            url = reverse('admin:api_product_change', args=[obj.product.id])
            return format_html('<a href="{}">{}</a>', url, obj.product)
        return "-"
    
    product_link.short_description = 'Product'


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    form = VariantForm
    list_display = ('name', 'product_name', 'product_link')
    list_display_links = ('name', 'product_name')
    fieldsets = (
        (None, {
            'fields': ('name', 'product_name', 'description', 'product')
        }),
    )

    def product_link(self, obj):
        # Create a link to the Product admin change page
        url = reverse('admin:api_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product)
    
    product_link.short_description = 'Product'


@admin.register(VariantImage)
class VariantImageAdmin(admin.ModelAdmin):
    form = VariantImageAdminForm
    list_display = ('id', 'image', 'variant_link', 'is_main')
    list_display_links = ('id', 'image')

    def variant_link(self, obj):
        if obj.variant:
            url = reverse('admin:api_variant_change', args=[obj.variant.id])
            return format_html('<a href="{}">{}</a>', url, obj.variant)
        return "-"
    
    variant_link.short_description = 'Variant'


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    form = StatForm  # If you have a custom form
    list_display = ('name', 'number', 'unit', 'additional', 'variant_link')
    list_display_links = ('name',)
    search_fields = ('name', 'number', 'unit', 'additional')

    def variant_link(self, obj):
        if obj.variant:
            url = reverse('admin:api_variant_change', args=[obj.variant.id])
            return format_html('<a href="{}">{}</a>', url, obj.variant)
        return "-"
    
    variant_link.short_description = 'Variant'


@admin.register(AudioTrack)
class AudioTrackAdmin(admin.ModelAdmin):
    form = AudioTrackForm  # If you have a custom form
    list_display = ('name', 'variant_link')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('variant',)

    def variant_link(self, obj):
        if obj.variant:
            url = reverse('admin:api_variant_change', args=[obj.variant.id])
            return format_html('<a href="{}">{}</a>', url, obj.variant)
        return "-"
    
    variant_link.short_description = 'Variant'