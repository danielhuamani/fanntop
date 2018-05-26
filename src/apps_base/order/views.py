from django.shortcuts import render
from django.db.models import Count, Sum, Q, F, Subquery, FloatField, CharField, Value as V
from django.db.models.functions import Concat
from rest_framework import viewsets
from apps_base.core.mixins import BaseAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderDetail
from .serializers import OrderSerializer
from apps_base.core.mixins import StandardPagination
from apps_base.product.models import Product
from apps_base.promotion.models import Coupon
from apps_base.order.constants import PAGADO
from apps_base.core.utils import range_month, format_date, range_start_end, month_initial, today_date, daterange
import locale


class OrderViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Order.objects.all().annotate(full_name=Concat(
        'order_order_customer__first_name', V(' '), 'order_order_customer__last_name',
        output_field=CharField())).annotate(email=F(
        'order_order_customer__email')).prefetch_related('order_ordershipping',
        'order_ordershipping__ubigeo', 'order_orderdetail', 'order_order_customer',
        'order_orderdetail__productdetail',
        'order_orderdetail__productdetail__product_product_images__product_image'
        ).order_by('-created')
    serializer_class = OrderSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        query_data = self.request.query_params
        search = query_data.get('search', None)
        field = query_data.get('field', None)
        orderBy = query_data.get('orderBy', None)
        total_to = query_data.get('total_to')
        total_from = query_data.get('total_from')
        create_from = query_data.get('create_from')
        create_to = query_data.get('create_to')
        status = query_data.get('status')
        if search:
            queryset = queryset.filter(
                Q(order_order_customer__first_name__icontains=search) |
                Q(order_order_customer__last_name__icontains=search) |
                Q(order_order_customer__email__icontains=search))
        if total_to:
            queryset = queryset.filter(total__lte=float(total_to))
        if total_from:
            queryset = queryset.filter(total__gte=float(total_from))
        if create_to:
            queryset = queryset.filter(created__lte=format_date(create_to))
        if create_from:
            queryset = queryset.filter(created__gte=format_date(create_from))
        if status:
            queryset = queryset.filter(type_status_shipping=status)
        if field:
            if orderBy == 'desc':
                ordering = '{0}{1}'.format('-', field)
                queryset = queryset.order_by(ordering)
            else:
                queryset = queryset.order_by(field)

        return queryset

class OrderDashboardHeaderAPI(BaseAuthenticated, APIView):
    def get(self, request, format=None):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        user = self.request.user
        today = today_date()
        month = month_initial()
        queryset_order = Order.objects.filter(type_status=PAGADO)
        total_sales_month = queryset_order.filter(created__date__gte=month).aggregate(total_sales_month=Sum('total'))
        total_sales_month = total_sales_month.get('total_sales_month')
        if not total_sales_month:
            total_sales_month = 0
        total_sales_date = queryset_order.filter(created__date__gte=today).aggregate(total_sales_date=Sum('total'))
        total_sales_date = total_sales_date.get('total_sales_date', 0)
        total_product = OrderDetail.objects.filter(id__in=queryset_order.values_list('id', flat=True)).count()
        if not total_sales_date:
            total_sales_date = 0
        data = {
            'month': month.strftime("%B %Y").title(),
            'day': today.strftime("%d %B %Y").title(),
            'total_sales_month': total_sales_month,
            'total_sales_date': total_sales_date,
            'total_order_month': queryset_order.filter(created__date__gte=month).count(),
            'total_product': total_product
            # 'total_product': queryset_product.count()
        }
        return Response(data)


class OrderDashboardFooterAPI(BaseAuthenticated, APIView):
    def get(self, request, format=None):
        skus = Product.objects.filter(is_active=True).count()
        coupon = Coupon.objects.filter(is_active=True).count()
        data = {
            'skus': skus,
            'coupon': coupon

            # 'total_product': queryset_product.count()
        }
        return Response(data)


class OrderDashboardSalesAPI(BaseAuthenticated, APIView):

    def get(self, request, format=None):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        user = self.request.user
        list_sum_total = []
        list_mes_anio = []
        create_from = self.request.query_params.get('create_from')
        create_to = self.request.query_params.get('create_to')
        queryset = Order.objects.filter(type_status=PAGADO)
            # influencer_json=RawSQL(
            #     "(shipping_influencer->%s->%s)::text",
            #     (shipping_influencer, 'total_influencer'))).annotate(
            #     influencer_total=Cast('influencer_json', FloatField())).prefetch_related(
            #     'order_order_customer', 'order_ordershipping', 'order_orderdetail').distinct('id')
        for day in daterange(create_from, create_to):
            order_day = queryset.filter(
                created__date__gte=day.get('mes_start')
            )
            if day.get('mes_end'):
                order_day = order_day.filter(created__date__lt=day.get('mes_end'))
            order_day = order_day.aggregate(total_fecha=Sum('total'))
            mes_anio = day.get('mes_start').strftime("%d %b %y").title()
            # mes_anio_end = day.get('mes_end').strftime("%d %b %y").title()
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


class OrderDashboardCountAPI(BaseAuthenticated, APIView):

    def get(self, request, format=None):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        user = self.request.user
        list_reporte_mes = []
        create_from = self.request.query_params.get('create_from')
        create_to = self.request.query_params.get('create_to')
        create_from = format_date(create_from)
        create_to = format_date(create_to)
        status = [
            {
                'value': 'AL',
                'name': 'En Almacén'
            },
            {
                'value': 'DS',
                'name': 'En Despacho'
            },
            {
                'value': 'EG',
                'name': 'Entregado'
            }
        ]
        queryset = Order.objects.filter(type_status=PAGADO)
        queryset = queryset.distinct('id')
        for st in status:
            queryset_status = queryset.filter(
                type_status_shipping=st.get('value'),
                created__date__lte=create_to,
                created__date__gte=create_from
            ).count()
            list_reporte_mes.append({
                'name': st.get('name'),
                'total': queryset_status
            })
        # month_start, month_end = range_start_end()
        data = {
            'mes_anio': create_from.strftime("%d %b %y").title() + " - " + create_to.strftime("%d %b %y").title(),
            'reporte': list_reporte_mes
        }
        return Response(data)