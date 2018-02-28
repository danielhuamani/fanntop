from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from apps_base.product.models import ProductClass, Product
from apps_base.category.models import Category
from apps_base.influencer.models import Influencer
from apps_base.attribute.models import Attribute
from .serializers import (ProductClassSerializer, InfluencerFilterSerializer,
    AttributeFilterSerializer, ProductClassDetailSerializer, ProductClassAttrSerializer)
from .utils import ProductPagination


class ProductClassCategoryListAPI(ListAPIView):
    queryset = ProductClass.objects.active().filter(is_published=True).select_related('influencer').prefetch_related(
        'product_class_products', 'category')
    serializer_class = ProductClassSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')
        slug_child = self.kwargs.get('slug_child')
        category = Category.objects.get(slug=slug_child)
        # category = get_object_or_404(Category, category__slug=slug, slug=slug_child)
        queryset = queryset.filter(category=category)
        filter_influencer = self.request.query_params.getlist('influencer[]', None)
        filter_attribute = self.request.query_params.getlist('attr[]', None)
        if filter_influencer:
            queryset = queryset.filter(influencer__slug__in=filter_influencer)
        for attr in filter_attribute:
            str_attr = '{0}{1}'.format(attr, '[]')
            attr_slug = self.request.query_params.getlist(str_attr, None)
            queryset = queryset.filter(product_class_products__attribute_option__slug__in=attr_slug).distinct('id')
        return queryset


class CategoryFilterAPI(APIView):
    queryset = ProductClass.objects.active().filter(is_published=True).select_related('influencer')

    def get(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        slug_child = self.kwargs.get('slug_child')
        category = get_object_or_404(Category, category__slug=slug, slug=slug_child)
        product_class = ProductClass.objects.active().filter(is_published=True, category=category)
        product_class_ids = product_class.values_list('id', flat=True)
        product_class_influencer_ids = product_class.values_list('influencer_id', flat=True)
        filter_influencer = self.request.query_params.getlist('influencer[]', None)
        if filter_influencer:
            queryset = product_class.filter(influencer__slug__in=filter_influencer)

        product_ids = Product.objects.filter(
            product_class_id__in=product_class_ids, attribute_option__id__isnull=False)

        products_attribute_option_ids = product_ids.filter(
            attribute_option__attribute__is_variation=True).distinct(
            'attribute_option__id').values_list('attribute_option__id', flat=True)
        products_attribute_ids = product_ids.distinct(
            'attribute_option__attribute__id').values_list('attribute_option__attribute__id', flat=True)
        attributes = Attribute.objects.filter(is_variation=True, id__in=products_attribute_ids)
        serializer_attribute = AttributeFilterSerializer(attributes, many=True, context={
            'attribute_option_ids': products_attribute_option_ids}).data
        influencers = Influencer.objects.filter(id__in=list(product_class_influencer_ids))
        serializer_influencer = InfluencerFilterSerializer(influencers, many=True).data
        data = {
            'influencers': serializer_influencer,
            'attributes': serializer_attribute
        }
        return Response(data)


class ProductClassListAPI(ListAPIView):
    queryset = ProductClass.objects.active().filter(is_published=True).select_related('influencer')
    serializer_class = ProductClassSerializer
    lookup_field = 'slug'


class ProductClassAttrAPI(APIView):
    queryset = ProductClass.objects.active().filter(is_published=True).select_related('influencer')
    lookup_field = 'slug'

    def get_object(self, slug):
        return get_object_or_404(ProductClass, slug=slug)

    def get(self, request, slug, format=None):
        product_class = self.get_object(slug)
        attributes = product_class.attribute.all()
        attribute_option = []
        for product in product_class.product_class_products.all().prefetch_related('attribute_option'):
            attribute_option += product.attribute_option.all().values_list('id', flat=True)
        serializer_attribute = AttributeFilterSerializer(attributes, many=True, context={
            'attribute_option_ids': attribute_option})
        serializer = ProductClassAttrSerializer(product_class, context={'request': self.request})
        data = {
            'product_class': serializer.data,
            'attributes': serializer_attribute.data
        }
        return Response(data)


class ProductClassDetailAPI(APIView):
    # queryset = ProductClass.objects.active().filter(is_published=True).select_related('influencer')
    lookup_field = 'slug'

    def get_object(self, slug):
        return get_object_or_404(ProductClass, slug=slug)

    def get(self, request, slug, format=None):
        product_class = self.get_object(slug)
        serializer = ProductClassDetailSerializer(product_class, context={'request': self.request})
        return Response(serializer.data)
    # lookup_field = slug
    # def get(self, request, format=None):
    #     snippets = Snippet.objects.all()
    #     serializer = ProductClassSerializer(snippets, many=True)
    #     return Response(serializer.data)