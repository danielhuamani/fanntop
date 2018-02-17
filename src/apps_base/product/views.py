from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import mixins
from .models import ProductClass, Product, ProductGaleryImage, ProductImage
from apps_base.core.mixins import BaseAuthenticated
from .serializers import ProductClassSerializer, ProductSerializer, ProductGaleryImageSerializer, ProductImageSerializer, ProductClassAttributeSerializer
from apps_base.attribute.serializers import AttributeSerializer
from apps_base.attribute.models import Attribute
from apps_base.family.serializers import FamilyGroupSerializer
from apps_base.family.models import Family, FamilyGroup, FamilyAttribute
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


class ProductClassViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductClass.objects.all()
    serializer_class = ProductClassSerializer


class ProductImageViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product_id', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        else:
            queryset = queryset.none()
        return queryset


class ProductViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Product.objects.not_trash()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product_class_id = self.request.query_params.get('product_class_id', None)
        if product_class_id:
            queryset = queryset.filter(product_class_id=int(product_class_id))
        return queryset


class ProductGaleryImageViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    queryset = ProductGaleryImage.objects.all()
    serializer_class = ProductGaleryImageSerializer


class ProductAttributeAPI(BaseAuthenticated, ListAPIView):
    queryset = Attribute.objects.filter(is_variation=True)
    serializer_class = AttributeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        family_id = self.request.query_params.get('family', None)
        attribute_ids = self.request.query_params.getlist('attribute_ids[]', None)
        if attribute_ids:
            queryset = queryset.filter(id__in=attribute_ids)
        elif family_id:
            attribute_ids = FamilyAttribute.objects.filter(family__id=family_id)
            queryset = queryset.filter(id__in=list(attribute_ids.values_list('attribute_id', flat=True)))
        else:
            queryset = queryset.none()
        return queryset


class ProductFamilyAttributeAPI(BaseAuthenticated, ListAPIView):
    queryset = FamilyGroup.objects.all()
    serializer_class = FamilyGroup

    def get_queryset(self):
        queryset = super().get_queryset()
        family_id = self.request.query_params.get('family', None)
        if family_id:
            queryset = queryset.filter(family_id=int(family_id))
        else:
            queryset = queryset.none()
        return queryset


class ProductClassAttributeAPI(BaseAuthenticated, RetrieveAPIView):
    queryset = ProductClass.objects.all()
    serializer_class = ProductClassAttributeSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     family_id = self.request.query_params.get('family', None)
    #     if family_id:
    #         queryset = queryset.filter(family_id=int(family_id))
    #     else:
    #         queryset = queryset.none()
    #     return queryset