from django.shortcuts import render
from django.db.models.expressions import RawSQL
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from django.db.models import Count, Sum, Case, Q, F, Subquery, Value, When, FloatField, CharField, Value as V
from django.db.models.functions import Cast, Concat
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from .serializers.system import (UserInfluencerJSONWebTokenSerializer, UserSerializer,
    UserChangePassSerializer)
from .serializers.product import ProductClassSerializer
from .serializers.order import OrderSerializer
from .mixins import StandardPagination
from apps_base.core.mixins import BaseInfluencerAuthenticated
from apps_base.product.models import Product, ProductClass
from apps_base.order.models import Order
from apps_base.order.constants import PAGADO
from rest_framework_jwt.views import JSONWebTokenAPIView
from .utils import range_month, format_date
import locale
import json


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


class OrderListAPI(BaseInfluencerAuthenticated, ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        user = self.request.user
        user_influencer = user.user_user_influencer
        shipping_influencer = str(user_influencer.influencer_id)
        shipping_influencer__price = 'shipping_influencer__' + shipping_influencer + '__total'
        queryset_initial = Order.objects.filter(type_status=PAGADO,
            order_orderdetail__productdetail__product_class__influencer__id=user_influencer.influencer_id
            )
        search = self.request.query_params.get('search', None)
        field = self.request.query_params.get('field', None)
        orderBy = self.request.query_params.get('orderBy', None)
        filters = self.request.query_params.get('filter', None)

        if search:
            queryset_initial = queryset_initial.filter(
                Q(order_order_customer__first_name__icontains=search) |
                Q(order_order_customer__last_name__icontains=search) |
                Q(order_order_customer__email__icontains=search))
        order_ids = queryset_initial.distinct('id').values_list('id', flat=True)
        queryset = Order.objects.filter(
            id__in=order_ids
            ).annotate(full_name=Concat(
                'order_order_customer__first_name', V(' '), 'order_order_customer__last_name',
                output_field=CharField())).prefetch_related(
                'order_order_customer', 'order_ordershipping', 'order_orderdetail').annotate(influencer_json=RawSQL(
                    "(shipping_influencer->%s->%s)::text",
                    (shipping_influencer, 'total'))).annotate(
                    influencer_total=Cast('influencer_json', FloatField()))
        if filters:
            filters = json.loads(filters)
            total_to = filters.get('total_to')
            total_from = filters.get('total_from')
            create_from = filters.get('create_from')
            create_to = filters.get('create_to')
            status = filters.get('status')
            if total_to:
                queryset = queryset.filter(influencer_total__lte=float(total_to))
            if total_from:
                queryset = queryset.filter(influencer_total__gte=float(total_from))
            if create_to:
                queryset = queryset.filter(created__lte=format_date(create_to))
            if create_from:
                queryset = queryset.filter(created__gte=format_date(create_from))
            if status:
                queryset = queryset.filter(type_status_shipping__in=status)
        if field:
            if field == 'influencer_total':
                ordering = field
                if orderBy == 'desc':
                    ordering = '{0}{1}'.format('-', field)
                queryset = queryset.order_by(ordering)
            else:
                if orderBy == 'desc':
                    ordering = '{0}{1}'.format('-', field)
                    queryset = queryset.order_by(ordering)
                else:
                    queryset = queryset.order_by(field)

        return queryset

    def get_serializer_context(self):
        user = self.request.user
        user_influencer = user.user_user_influencer
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'influencer_id': user_influencer.influencer_id
        }

class OrderDetailAPI(BaseInfluencerAuthenticated, RetrieveAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'code'

    def get_queryset(self):
        user = self.request.user
        user_influencer = user.user_user_influencer
        shipping_influencer = str(user_influencer.influencer_id)
        queryset = Order.objects.filter(
            type_status=PAGADO,
            order_orderdetail__productdetail__product_class__influencer__id=user_influencer.influencer_id).distinct('id')
            # influencer_json=RawSQL(
            #     "(shipping_influencer->%s->%s)::text",
            #     (shipping_influencer, 'total_influencer'))).annotate(
            #     influencer_total=Cast('influencer_json', FloatField())).prefetch_related(
            #     'order_order_customer', 'order_ordershipping', 'order_orderdetail').distinct('id')
        print(queryset, 'queryset')
        return queryset

    def get_serializer_context(self):
        user = self.request.user
        user_influencer = user.user_user_influencer
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'influencer_id': user_influencer.influencer_id
        }


class UserAPI(BaseInfluencerAuthenticated, RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        return user


class UserChangePassAPI(BaseInfluencerAuthenticated, UpdateAPIView):
    serializer_class = UserChangePassSerializer

    def get_object(self):
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("password")):
                return Response({"password": ["Wrong password."]}, status=403)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({}, status=200)

        return Response(serializer.errors, status=403)


class DashboardaAPI(BaseInfluencerAuthenticated, APIView):

    def get(self, request, format=None):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        user = self.request.user
        user_influencer = user.user_user_influencer
        shipping_influencer = str(user_influencer.influencer_id)
        list_sum_total = []
        list_mes_anio = []
        queryset = Order.objects.filter(
            type_status=PAGADO,
            order_orderdetail__productdetail__product_class__influencer__id=user_influencer.influencer_id).annotate(influencer_json=RawSQL(
                "(shipping_influencer->%s->%s)::text",
                (shipping_influencer, 'total'))).annotate(
                influencer_total=Cast('influencer_json', FloatField()))
            # influencer_json=RawSQL(
            #     "(shipping_influencer->%s->%s)::text",
            #     (shipping_influencer, 'total_influencer'))).annotate(
            #     influencer_total=Cast('influencer_json', FloatField())).prefetch_related(
            #     'order_order_customer', 'order_ordershipping', 'order_orderdetail').distinct('id')
        for day in range_month():
            order_day = queryset.filter(
                created__date__gte=day.get('mes_start'),
                created__date__lt=day.get('mes_end')

            ).aggregate(total_fecha=Sum('influencer_total'))
            mes_anio = day.get('mes_start').strftime("%b %y").title()
            sum_anio = order_day.get('total_fecha')
            if not sum_anio:
                sum_anio = 0
            list_mes_anio.append(mes_anio)
            list_sum_total.append(sum_anio)
        data = {
            'mes_anio': list_mes_anio,
            'sum_total': list_sum_total
        }
        return Response(data)