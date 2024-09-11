from django.db.models import Exists, OuterRef
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
from .serializers import (
    ContentTypeSerializer,
    MakeSerializer, 
    ModelSerializer, 
    ProductSerializer, 
    ProductMakeModelConnectionSerializer, 
    VariantSerializer, 
    VariantImageSerializer,
    StatSerializer,
    AudioTrackSerializer
)
from django.contrib.contenttypes.models import ContentType

# Helper function to cache ContentType lookups
def get_cached_content_type(model):
    cache_key = f"content_type_{model._meta.app_label}_{model._meta.model_name}"
    content_type = cache.get(cache_key)
    if not content_type:
        content_type = ContentType.objects.get_for_model(model)
        cache.set(cache_key, content_type)
    return content_type

# Cache for 1 hour
CACHE_TIME = 60 * 60

# ContentType List API
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class ContentTypeListAPIView(generics.ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

# Cache Make List for 1 hour
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class MakeListAPIView(generics.ListAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer

# Get Makes by Product
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class MakesByProductView(generics.GenericAPIView):
    serializer_class = MakeSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if not product_id:
            return Make.objects.none()

        make_ids = ProductMakeModelConnection.objects.filter(
            product_id=product_id,
            parent_type=ContentType.objects.get_for_model(Make)
        ).values_list('parent_id', flat=True)

        return Make.objects.filter(id__in=make_ids)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            raise NotFound(detail="Makes not found for the given Product ID")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Car Model List
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class ModelListAPIView(generics.ListAPIView):
    queryset = CarModel.objects.all().select_related('parent_type')  # Pre-fetch ContentType
    serializer_class = ModelSerializer

# CarModel by Make View
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class CarModelByMakeView(generics.GenericAPIView):
    serializer_class = ModelSerializer

    def get_queryset(self):
        make_id = self.kwargs.get('make_id')
        if not make_id:
            return CarModel.objects.none()

        content_type = get_cached_content_type(Make)

        return CarModel.objects.filter(
            parent_id=make_id,
            parent_type=content_type
        ).select_related('parent_type')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            raise NotFound(detail="CarModels not found for the given Make ID")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# CarModel by Model View
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class CarModelByModelView(generics.GenericAPIView):
    serializer_class = ModelSerializer

    def get_queryset(self):
        model_id = self.kwargs.get('model_id')
        if not model_id:
            return CarModel.objects.none()

        content_type = get_cached_content_type(CarModel)

        return CarModel.objects.filter(
            parent_id=model_id,
            parent_type=content_type
        ).select_related('parent_type')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            raise NotFound(detail="CarModels not found for the given Model ID")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Models by Product View
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class ModelsByProductView(generics.GenericAPIView):
    serializer_class = ModelSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if not product_id:
            return CarModel.objects.none()

        carmodel_ids = ProductMakeModelConnection.objects.filter(
            product_id=product_id,
            parent_type=ContentType.objects.get_for_model(CarModel)
        ).values_list('parent_id', flat=True)
    
        return CarModel.objects.filter(id__in=carmodel_ids)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            raise NotFound(detail="CarModels not found for the given Product ID")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Product List API
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# ProductMakeModelConnection List
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class ProductMakeModelConnectionListView(generics.ListCreateAPIView):
    queryset = ProductMakeModelConnection.objects.all()
    serializer_class = ProductMakeModelConnectionSerializer

# Products by Make
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class ProductsByMakeView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        make_id = self.kwargs.get('make_id')
        if not make_id:
            return Product.objects.none()

        content_type = get_cached_content_type(Make)
        return Product.objects.filter(
            productmakemodelconnection__parent_id=make_id,
            productmakemodelconnection__parent_type=content_type
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            raise NotFound(detail="Products not found for the given Make ID")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Products by Model View
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class ProductsByModelView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        model_id = self.kwargs.get('model_id')
        if not model_id:
            return Product.objects.none()

        content_type = get_cached_content_type(CarModel)
        return Product.objects.filter(
            productmakemodelconnection__parent_id=model_id,
            productmakemodelconnection__parent_type=content_type
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            raise NotFound(detail="Products not found for the given Model ID")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Products with at least one variant and at least one image associated with a variant
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class ProductsWithVariantImageView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Check if a product has at least one variant with at least one image
        variant_with_image_qs = VariantImage.objects.filter(variant=OuterRef('id'))
        variants_with_images = Variant.objects.filter(product_id=OuterRef('pk')).filter(Exists(variant_with_image_qs))
        
        # Filter products that have variants with images
        return Product.objects.filter(Exists(variants_with_images))

# Variant List View
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class VariantListView(generics.ListAPIView):
    serializer_class = VariantSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if product_id:
            return Variant.objects.filter(product_id=product_id).select_related('product')
        
        return Variant.objects.all().select_related('product')

# Variant Detail View
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class VariantDetailView(generics.RetrieveAPIView):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer

# Variants by product ID that have at least one image
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class VariantsWithImageByProductView(generics.ListAPIView):
    serializer_class = VariantSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        
        if not product_id:
            return Variant.objects.none()
        
        # Query to find variants with at least one image
        variant_with_image_qs = VariantImage.objects.filter(variant=OuterRef('id'))
        
        # Filter variants that belong to the specified product and have images
        return Variant.objects.filter(product_id=product_id).filter(Exists(variant_with_image_qs))

# Variant Image List View
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class VariantImageListView(generics.ListAPIView):
    queryset = VariantImage.objects.all()
    serializer_class = VariantImageSerializer

# Variant Images by Product
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class VariantImagesByVariantView(generics.ListAPIView):
    serializer_class = VariantImageSerializer

    def get_queryset(self):
        variant_id = self.kwargs.get('variant_id')
        if not variant_id:
            return VariantImage.objects.none()

        return VariantImage.objects.filter(variant_id=variant_id).select_related('variant')

# Stat List View
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class StatListAPIView(generics.ListAPIView):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer

# Stats by Variant
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class StatByVariantAPIView(generics.ListAPIView):
    serializer_class = StatSerializer

    def get_queryset(self):
        variant_id = self.kwargs['variant_id']
        return Stat.objects.filter(variant_id=variant_id).select_related('variant')

# Audio Track List View
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class AudioTrackListAPIView(generics.ListAPIView):
    queryset = AudioTrack.objects.all()
    serializer_class = AudioTrackSerializer

# Audio Tracks by Variant
@method_decorator(cache_page(CACHE_TIME), name='dispatch')
class AudioTrackByVariantAPIView(generics.ListAPIView):
    serializer_class = AudioTrackSerializer

    def get_queryset(self):
        variant_id = self.kwargs['variant_id']
        return AudioTrack.objects.filter(variant_id=variant_id).select_related('variant')
