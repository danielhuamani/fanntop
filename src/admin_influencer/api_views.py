from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers.system import UserInfluencerJSONWebTokenSerializer
from .serializers.product import ProductClassSerializer
from .mixins import StandardPagination
from apps_base.core.mixins import BaseInfluencerAuthenticated
from apps_base.product.models import Product, ProductClass
from rest_framework_jwt.views import JSONWebTokenAPIView


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = UserInfluencerJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()


class ProductListAPI(BaseInfluencerAuthenticated, ListAPIView):
    serializer_class = ProductClassSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        user = self.request.user
        user_influencer = user.user_user_influencer
        queryset = ProductClass.objects.filter(
            influencer_id=user_influencer.influencer_id).prefetch_related(
            'product_class_products', 'product_class_products__attribute_option')
        search = self.request.query_params.get('search', None)
        field = self.request.query_params.get('field', None)
        orderBy = self.request.query_params.get('orderBy', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if field:
            if field == 'product_class_products__price':
                ordering = field
                if orderBy == 'desc':
                    ordering = '{0}{1}'.format('-', field)
                queryset = queryset.order_by(ordering)
                queryset = ProductClass.objects.filter(id__in=queryset.values_list('id', flat=True))
            else:
                if orderBy == 'desc':
                    ordering = '{0}{1}'.format('-', field)
                    queryset = queryset.order_by(ordering)
                else:
                    queryset = queryset.order_by(field)

        return queryset


class ProductDetailAPI(BaseInfluencerAuthenticated, RetrieveAPIView):
    serializer_class = ProductClassSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        user_influencer = user.user_user_influencer
        queryset = ProductClass.objects.filter(
            influencer_id=user_influencer.influencer_id).prefetch_related(
            'product_class_products', 'product_class_products__attribute_option')
        return queryset