from django.urls import path
from .views import (
    ContentTypeListAPIView,
    MakeListAPIView,
    MakesByProductView,
    ModelListAPIView,
    CarModelByMakeView,
    CarModelByModelView,
    ModelsByProductView,
    ProductListView,
    ProductsByMakeView,
    ProductsByModelView,
    ProductMakeModelConnectionListView,
    VariantListView,
    VariantDetailView,
    VariantImageListView,
    VariantImagesByVariantView,
    StatListAPIView,
    StatByVariantAPIView,
    AudioTrackListAPIView,
    AudioTrackByVariantAPIView
)


urlpatterns = [
    path('contenttypes/', ContentTypeListAPIView.as_view(), name='contenttype-list'),

    path('makes/', MakeListAPIView.as_view(), name='make-list'),
    path('makes/product/<int:product_id>/', MakesByProductView.as_view(), name='makes-by-product'),

    path('models/', ModelListAPIView.as_view(), name='model-list'),
    path('models/make/<int:make_id>/', CarModelByMakeView.as_view(), name='carmodel-by-make'),
    path('models/model/<int:model_id>/', CarModelByModelView.as_view(), name='carmodel-by-model'),
    path('models/product/<int:product_id>/', ModelsByProductView.as_view(), name='models-by-product'),

    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/make/<int:make_id>/', ProductsByMakeView.as_view(), name='products-by-make'),
    path('products/model/<int:model_id>/', ProductsByModelView.as_view(), name='products-by-model'),

    path('productconnections/', ProductMakeModelConnectionListView.as_view(), name='product-connection-list'),

    path('variants/', VariantListView.as_view(), name='variant-list'),
    path('variants/<int:pk>/', VariantDetailView.as_view(), name='variant-detail'),
    path('variants/product/<int:product_id>', VariantListView.as_view(), name='variants-by-product'),

    path('variantimages/', VariantImageListView.as_view(), name='variant-image-list'),
    path('variantimages/variant/<int:variant_id>', VariantImagesByVariantView.as_view(), name='variant-images-by-variant'),

    path('stats/', StatListAPIView.as_view(), name='stat-list'),
    path('stats/variant/<int:variant_id>/', StatByVariantAPIView.as_view(), name='stats-by-variant'),

    path('audiotracks/', AudioTrackListAPIView.as_view(), name='audiotrack-list'),
    path('audiotracks/variant/<int:variant_id>/', AudioTrackByVariantAPIView.as_view(), name='audiotracks-by-variant'),
]