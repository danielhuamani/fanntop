from django.shortcuts import render
from django.db.models import Count, Sum, Q, F, Subquery, FloatField, CharField, Value as V
from rest_framework import viewsets
from apps_base.core.mixins import BaseAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer
from apps_base.order.constants import PAGADO
from apps_base.core.utils import range_month, format_date, range_start_end, month_initial, today_date, daterange
import locale


class OrderViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Order.objects.all().prefetch_related('order_ordershipping',
        'order_ordershipping__ubigeo', 'order_orderdetail', 'order_order_customer',
        'order_orderdetail__productdetail',
        'order_orderdetail__productdetail__product_product_images__product_image'
        ).order_by('-created')
    serializer_class = OrderSerializer


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
        if not total_sales_date:
            total_sales_date = 0
        data = {
            'month': month.strftime("%B %Y").title(),
            'day': today.strftime("%d %B %Y").title(),
            'total_sales_month': total_sales_month,
            'total_sales_date': total_sales_date,
            'total_order_month': queryset_order.filter(created__date__gte=month).count(),
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