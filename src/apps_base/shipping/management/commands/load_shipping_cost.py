
from django.core.management.base import BaseCommand

import json
from apps_base.shipping.models import ShippingCost
from apps_base.ubigeo.models import Ubigeo
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        LIMA = 15
        LIMA_COST = 10
        LIMA_EXCLUDE_COST = 15
        ShippingCost.objects.all().delete()
        ubigeo_lima = Ubigeo.objects.filter(cod_dep_inei=15)
        ubigeo_exclude_lima = Ubigeo.objects.exclude(cod_dep_inei=15)
        print(ubigeo_lima)
        list_shipping_cost = []
        for lima in ubigeo_lima:
            print(lima, 'lima')
            list_shipping_cost.append(
                ShippingCost(
                    ubigeo=lima,
                    price=LIMA_COST
                )
            )
        for lima in ubigeo_exclude_lima:
            print(lima, 'fuera')
            list_shipping_cost.append(
                ShippingCost(
                    ubigeo=lima,
                    price=LIMA_COST
                )
            )
        ShippingCost.objects.bulk_create(list_shipping_cost)