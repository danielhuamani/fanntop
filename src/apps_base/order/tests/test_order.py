from django.test import TestCase
from apps_base.influencer.models import Influencer
from apps_base.product.models import ProductClass, Product
from apps_base.order.models import Order, OrderDetail
from apps_base.promotion.models import Coupon


class OrderTestCase(TestCase):

    def setUp(self):
        self.influencer_one = Influencer.objects.create(name='influencer 1')
        self.influencer_two = Influencer.objects.create(name='influencer 2')