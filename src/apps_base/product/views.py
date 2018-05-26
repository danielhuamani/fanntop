from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Q
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
from apps_base.core.mixins import StandardPagination


class ProductClassViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductClass.objects.all().select_related('influencer')
    serializer_class = ProductClassSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        query_data = self.request.query_params
        search = query_data.get('search', None)
        field = query_data.get('field', None)
        orderBy = query_data.get('orderBy', None)
        price_to = query_data.get('price_to')
        price_from = query_data.get('price_from')
        create_from = query_data.get('create_from')
        create_to = query_data.get('create_to')
        is_published = query_data.get('is_published')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(influencer__name__icontains=search)
            )
        if price_to:
            queryset = queryset.filter(price__lte=float(price_to))
        if price_from:
            queryset = queryset.filter(price__gte=float(price_from))
        if is_published:
            if is_published == 'si':
                queryset = queryset.filter(is_published=True)
            elif is_published == 'no':
                queryset = queryset.filter(is_published=False)
        if field:
            if orderBy == 'desc':
                ordering = '{0}{1}'.format('-', field)
                queryset = queryset.order_by(ordering)
            else:
                queryset = queryset.order_by(field)

        return queryset

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