from django.db.models import Sum
from .models import Order, OrderDetail
from apps_base.shipping.models import ShippingCost
from apps_base.promotion.models import CouponGenerate, Coupon
from apps_base.order.constants import PROCESO
from decimal import Decimal as D, getcontext


class OrderGenerate(object):

    def get_discount_infuencer_coupon(self, coupon, discount, order):
        order_details = order.order_orderdetail.all()
        influencers = coupon.influencers.all()
        total_sum_influencer = order.order_orderdetail.filter(
            productdetail__product_class__influencer__in=influencers.values_list('id', flat=True)).aggregate(Sum('total'))
        total_sum = total_sum_influencer.get('total__sum')
        total_discount = discount
        shipping_influencer = {}
        for influencer in influencers:
            total_influencer = order_details.filter(
                productdetail__product_class__influencer__id=influencer.id)
            if total_influencer.exists():
                total_influencer = total_influencer.aggregate(Sum('total')).get('total__sum', 0)
                percentage = float(total_influencer / total_sum)
                shipping_influencer[influencer.id] = {
                    'discount': 0,
                    'name': influencer.name,
                    'total_sum': float(total_sum),
                    'percentage': percentage * float(100),
                    'total': total_discount * percentage
                }
        return shipping_influencer
        #     pass
        # shipping_influencer
        # key : {'discount': 0, 'name': 'mox', 'percentage': 20}
    def create(self, cart, customer, ubigeo, coupon):

        # try:
        #     shipping = ShippingCost.objects.get(ubigeo=ubigeo)
        #     price = shipping.price
        # except Exception as e:
        #     price = 0
        print(coupon, 'coupon')
        try:
            coupon_generate = Coupon.objects.get(
                prefix=coupon.strip(),  is_active=True)
            print(coupon_generate, 'coupon_generate---')
            if coupon_generate.type_discount == 'PTJ':
                discount = (float(float(sub_total)*coupon_generate.discount) / 100)
            elif coupon_generate.type_discount == 'SLS':
                discount = coupon_generate.discount
        except Exception as e:
            coupon_generate = None
            discount = 0
        shipping = ShippingCost.objects.get(ubigeo=ubigeo)
        price = shipping.price
        total = cart.total + price - D(discount)
        order = Order.objects.create(
            customer=customer,
            cart=cart,
            sub_total=cart.total,
            total=total,
            discount=D(discount),
            shipping_price=price,
            type_status=PROCESO,
        )
        if coupon_generate:
            order.coupon_discount = coupon_generate
            order.save()
        self.create_details(cart, order)
        print(coupon_generate, 'coupon_generate')
        if coupon_generate:
            order.shipping_influencer = self.get_discount_infuencer_coupon(coupon_generate, discount, order)
            order.save()
        # raise
        return order

    def update(self, cart, ubigeo, coupon):
        getcontext().prec = 2
        try:
            coupon_generate = Coupon.objects.get(
                prefix=coupon.strip(), is_active=True)
            if coupon_generate.type_discount == 'PTJ':
                discount = (float(float(sub_total)*coupon_generate.discount) / 100)
            elif coupon_generate.type_discount == 'SLS':
                discount = coupon_generate.discount
        except Exception as e:
            coupon_generate = None
            discount = 0
        shipping = ShippingCost.objects.get(ubigeo=ubigeo)
        price = shipping.price
        total = D(cart.total + price) - D(discount)
        order = Order.objects.get(cart__code=cart.code)
        order.sub_total = cart.total
        order.discount = D(discount)
        order.total = total
        order.shipping_price = price
        order.type_status = PROCESO
        self.update_details(cart, order)
        if coupon_generate:
            order.coupon = coupon_generate
            shipping_influencer = self.get_discount_infuencer_coupon(coupon_generate, discount, order)
            order.shipping_influencer = self.get_discount_infuencer_coupon(coupon_generate, discount, order)
            order.save()
        order.save()
        return order

    def update_details(self, cart, order):
        for cart_item in cart.cart_items.all():
            try:
                order_detail = OrderDetail.objects.get(order=order, productdetail=cart_item.product)
                order_detail.quantity=cart_item.quantity
                order_detail.price=cart_item.product.price
                order_detail.sub_total=cart_item.cart_item_total
                order_detail.total=cart_item.cart_item_total
                order_detail.save()
            except Exception as e:
                order_detail = OrderDetail(
                    order=order,
                    productdetail=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    sub_total=cart_item.cart_item_total,
                    total=cart_item.cart_item_total,
                )
                order_detail.save()
        return None

    def create_details(self, cart, order):
        for cart_item in cart.cart_items.all():
            order_detail = OrderDetail(
                order=order,
                productdetail=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                sub_total=cart_item.cart_item_total,
                total=cart_item.cart_item_total,
            )
            order_detail.save()
        return None