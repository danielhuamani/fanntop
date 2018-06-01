from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Max, Min
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from apps_base.product.models import ProductClass, Product
from apps_base.category.models import Category
from apps_base.influencer.models import Influencer
from apps_base.attribute.models import Attribute
from .serializers import (ProductClassSerializer, InfluencerFilterSerializer,
    AttributeFilterSerializer, ProductClassDetailSerializer, ProductClassAttrSerializer, ProductDetailSerializer)
from .utils import ProductPagination
from apps_base.customers.models import CustomerProductFavorite
from decimal import Decimal


class ProductClassCategoryListAPI(ListAPIView):
    queryset = ProductClass.objects.active().filter(
        is_published=True).select_related('influencer').prefetch_related(
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
        filter_prices = self.request.query_params.getlist('prices[]', [])
        orderBy = self.request.query_params.get('orderBy')
        attr_list = []
        if filter_influencer:
            queryset = queryset.filter(influencer__slug__in=filter_influencer)
        if filter_prices:
            queryset = queryset.filter(price__lte=Decimal(filter_prices[1]),
                price__gte=Decimal(filter_prices[0]))
        for attr in filter_attribute:
            str_attr = '{0}{1}'.format(attr, '[]')
            attr_slug = self.request.query_params.getlist(str_attr, None)
            attr_list += attr_slug
        if attr_list:
            queryset_product_class = Product.objects.filter(
                attribute_option__slug__in=attr_list).distinct('product_class_id')
            queryset = queryset.filter(
                id__in=queryset_product_class.values_list('product_class_id', flat=True))
        if orderBy:
            if orderBy == 'name_asc':
                queryset = queryset.order_by('name')
            elif orderBy == 'name_desc':
                queryset = queryset.order_by('-name')
            elif orderBy == 'price_asc':
                queryset = queryset.order_by('price')
            elif orderBy == 'price_desc':
                queryset = queryset.order_by('-price')

        return queryset

    def get_serializer_context(self):
        filter_attribute = self.request.query_params.getlist('attr[]', None)
        attr_list = []
        for attr in filter_attribute:
            str_attr = '{0}{1}'.format(attr, '[]')
            attr_slug = self.request.query_params.getlist(str_attr, None)
            attr_list += attr_slug
        context = super().get_serializer_context()
        context['attr_list'] = attr_list
        return context

    # def list(self, request, *args, **kwargs):
    #     filter_attribute = self.request.query_params.getlist('attr[]', None)
    #     attr_list = []
    #     for attr in filter_attribute:
    #         str_attr = '{0}{1}'.format(attr, '[]')
    #         attr_slug = self.request.query_params.getlist(str_attr, None)
    #         attr_list += attr_slug
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         print('page', attr_list)
    #         serializer = self.get_serializer(page, many=True, context={'attr_list': attr_list})
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


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
        list_price = []
        queryset = self.queryset
        if filter_influencer:
            queryset = product_class.filter(influencer__slug__in=filter_influencer)
        prices = queryset.aggregate(Max('product_class_products__price'), Min('product_class_products__price'))
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
            'attributes': serializer_attribute,
            'prices': [
                prices.get('product_class_products__price__min', 0),
                prices.get('product_class_products__price__max', 0)
            ]
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
        # for product in product_class.product_class_products.all().prefetch_related('attribute_option'):
        #     attribute_option += product.attribute_option.all().values_list('id', flat=True)
        # print(attribute_option, product_class.product_class_products.all().values_list('attribute_option', flat=True))
        attribute_option = product_class.product_class_products.all().values_list('attribute_option', flat=True)
        serializer_attribute = AttributeFilterSerializer(attributes, many=True, context={
            'attribute_option_ids': attribute_option})
        serializer = ProductClassAttrSerializer(product_class, context={'request': self.request})
        data = {
            'product_class': serializer.data,
            'attributes': serializer_attribute.data
        }
        return Response(data)


class ProductDetailAPI(APIView):
    # queryset = ProductClass.objects.active().filter(is_published=True).select_related('influencer')
    lookup_field = 'slug'

    def get_object(self, slug):
        return get_object_or_404(ProductClass, slug=slug)

    def get(self, request, slug, format=None):
        product_details = Product.objects.filter(product_class__slug=slug).prefetch_related('attribute_option__attribute', 'product_product_images')
        if product_details.exists():
            attr = self.request.query_params.getlist('attr[]', None)
            attr_list = []
            for str_attr in attr:
                attr_slug = self.request.query_params.get(str_attr, None)
                product_details = product_details.filter(attribute_option__slug=attr_slug)
            if attr:
                product_detail = product_details.order_by('-is_featured').first()
            else:
                product_detail = product_details.filter(is_active=True).order_by('is_featured').first()
            serializer = ProductDetailSerializer(product_detail, context={'request': self.request})
            return Response(serializer.data, status=200)
        return Response({}, status=404)
    # lookup_field = slug
    # def get(self, request, format=None):
    #     snippets = Snippet.objects.all()
    #     serializer = ProductClassSerializer(snippets, many=True)
    #     return Response(serializer.data)


class ProductClassInfluencerListAPI(ListAPIView):
    queryset = ProductClass.objects.active().filter(is_published=True).select_related('influencer').prefetch_related(
        'product_class_products', 'category')
    serializer_class = ProductClassSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')
        influencer = Influencer.objects.get(slug=slug)
        # category = get_object_or_404(Category, category__slug=slug, slug=slug_child)
        queryset = queryset.filter(influencer=influencer)
        # filter_influencer = self.request.query_params.getlist('influencer[]', None)
        filter_attribute = self.request.query_params.getlist('attr[]', None)
        filter_prices = self.request.query_params.getlist('prices[]', [])
        orderBy = self.request.query_params.get('orderBy')
        attr_list = []
        for attr in filter_attribute:
            str_attr = '{0}{1}'.format(attr, '[]')
            attr_slug = self.request.query_params.getlist(str_attr, None)
            attr_list += attr_slug
        if attr_list:
            queryset_product_class = Product.objects.filter(
                attribute_option__slug__in=attr_list).distinct('product_class_id')
            queryset = queryset.filter(
                id__in=queryset_product_class.values_list('product_class_id', flat=True))
        if filter_prices:
            queryset = queryset.filter(price__lte=Decimal(filter_prices[1]),
                price__gte=Decimal(filter_prices[0]))
        if orderBy:
            if orderBy == 'name_asc':
                queryset = queryset.order_by('name')
            elif orderBy == 'name_desc':
                queryset = queryset.order_by('-name')
            elif orderBy == 'price_asc':
                queryset = queryset.order_by('price')
            elif orderBy == 'price_desc':
                queryset = queryset.order_by('-price')

        return queryset

    def get_serializer_context(self):
        filter_attribute = self.request.query_params.getlist('attr[]', None)
        attr_list = []
        for attr in filter_attribute:
            str_attr = '{0}{1}'.format(attr, '[]')
            attr_slug = self.request.query_params.getlist(str_attr, None)
            attr_list += attr_slug
        context = super().get_serializer_context()
        context['attr_list'] = attr_list
        return context


class InfluencerFilterAPI(APIView):
    queryset = ProductClass.objects.active().filter(is_published=True).select_related('influencer')

    def get(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        influencer = get_object_or_404(Influencer, slug=slug)
        queryset = self.queryset
        product_class = ProductClass.objects.active().filter(is_published=True, influencer=influencer)
        product_class_ids = product_class.values_list('id', flat=True)
        product_class_influencer_ids = product_class.values_list('influencer_id', flat=True)

        filter_influencer = self.request.query_params.getlist('influencer[]', None)
        if filter_influencer:
            queryset = product_class.filter(influencer__slug__in=filter_influencer)
        prices = queryset.aggregate(Max('price'), Min('price'))
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
            'attributes': serializer_attribute,
            'prices': [
                prices.get('price__min', 0),
                prices.get('price__max', 0)
            ]
        }
        return Response(data)

class CustomerProductFavoriteAPI(ListAPIView):
    queryset = ProductClass.objects.active().filter(is_published=True).select_related('influencer').prefetch_related(
        'product_class_products', 'category')
    serializer_class = ProductClassSerializer
    pagination_class = ProductPagination

    def post(self, *args, **kwargs):
        product_id = self.request.data.get('product_id')
        code_favorite = self.request.COOKIES.get('code_favorite', '')
        product = get_object_or_404(ProductClass, id=int(product_id))
        if self.request.user.is_authenticated():
            customer_product_favorite, created = CustomerProductFavorite.objects.get_or_create(
                customer=self.request.user.user_customer)
            customer_product_favorite.product_class.add(product)
            return Response({}, status=200)
        else:
            customer_product_favorite = CustomerProductFavorite.objects.filter(code=code_favorite)
            if customer_product_favorite.exists():
                customer_product_favorite = customer_product_favorite.first()
                customer_product_favorite.product_class.add(product)
                return Response({}, status=200)
            else:
                customer_product_favorite = CustomerProductFavorite(customer=None)
                customer_product_favorite.save()
                customer_product_favorite.product_class.add(product)
                response = Response({}, status=200)
                response.set_cookie('code_favorite', customer_product_favorite.code)
                return response

    def get_queryset(self):
        queryset = super().get_queryset()
        code_favorite = self.request.COOKIES.get('code_favorite', '')
        if self.request.user.is_authenticated():
            try:
                customer_product_favorite = get_object_or_404(
                    CustomerProductFavorite, customer=self.request.user.user_customer)
                queryset = customer_product_favorite.product_class.all()
            except Exception as e:
                queryset = queryset.none()
            return queryset
        else:
            customer_product_favorite = CustomerProductFavorite.objects.filter(code=code_favorite)
            if customer_product_favorite.exists():
                customer_product_favorite = customer_product_favorite.first()
                queryset = customer_product_favorite.product_class.all()
                return queryset
            else:
                return queryset.none()