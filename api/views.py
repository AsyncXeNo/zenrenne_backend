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


class MakeListAPIView(generics.ListAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer


class ModelListAPIView(generics.ListAPIView):
    queryset = CarModel.objects.all()
    serializer_class = ModelSerializer


class CarModelByMakeView(generics.GenericAPIView):
    serializer_class = ModelSerializer

    def get_queryset(self):
        make_id = self.kwargs.get('make_id')
        if not make_id:
            return CarModel.objects.none()  # Return empty queryset if no Make ID is provided

        # Filter CarModels based on the Make ID
        return CarModel.objects.filter(
            parent_id=make_id,
            parent_type=ContentType.objects.get_for_model(Make)
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            raise NotFound(detail="CarModels not found for the given Make ID")
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CarModelByModelView(generics.GenericAPIView):
    serializer_class = ModelSerializer

    def get_queryset(self):
        model_id = self.kwargs.get('model_id')
        if not model_id:
            return CarModel.objects.none()  # Return empty queryset if no Model ID is provided

        # Filter CarModels based on the parent Model ID
        return CarModel.objects.filter(
            parent_id=model_id,
            parent_type=ContentType.objects.get_for_model(CarModel)
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            raise NotFound(detail="CarModels not found for the given Model ID")
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductMakeModelConnectionListView(generics.ListCreateAPIView):
    queryset = ProductMakeModelConnection.objects.all()
    serializer_class = ProductMakeModelConnectionSerializer


class ProductsByMakeView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        make_id = self.kwargs.get('make_id')
        if not make_id:
            return Product.objects.none()  # Return an empty queryset if no Make ID is provided

        # Filter products based on the Make ID
        return Product.objects.filter(
            productmakemodelconnection__parent_id=make_id,
            productmakemodelconnection__parent_type=ContentType.objects.get_for_model(Make)
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            raise NotFound(detail="Products not found for the given Make ID")
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductsByModelView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        model_id = self.kwargs.get('model_id')
        if not model_id:
            return Product.objects.none()  # Return an empty queryset if no Model ID is provided

        # Filter products based on the Model ID
        return Product.objects.filter(
            productmakemodelconnection__parent_id=model_id,
            productmakemodelconnection__parent_type=ContentType.objects.get_for_model(CarModel)
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            raise NotFound(detail="Products not found for the given Model ID")
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class VariantListView(generics.ListAPIView):
    serializer_class = VariantSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Variant.objects.filter(product_id=product_id)

class VariantDetailView(generics.RetrieveAPIView):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


class VariantImageListView(generics.ListAPIView):
    queryset = VariantImage.objects.all()
    serializer_class = VariantImageSerializer


class VariantImagesByProductView(generics.ListAPIView):
    serializer_class = VariantImageSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if not product_id:
            return VariantImage.objects.none()

        # Filter images by product ID through the variant
        return VariantImage.objects.filter(variant__product_id=product_id)
    

class StatListAPIView(generics.ListAPIView):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer


class StatByVariantAPIView(generics.ListAPIView):
    serializer_class = StatSerializer

    def get_queryset(self):
        variant_id = self.kwargs['variant_id']
        return Stat.objects.filter(variant_id=variant_id)
    

class AudioTrackListAPIView(generics.ListAPIView):
    queryset = AudioTrack.objects.all()
    serializer_class = AudioTrackSerializer


class AudioTrackByVariantAPIView(generics.ListAPIView):
    serializer_class = AudioTrackSerializer

    def get_queryset(self):
        variant_id = self.kwargs['variant_id']
        return AudioTrack.objects.filter(variant_id=variant_id)