from .models import Order, OrderDetail
from apps_base.shipping.models import ShippingCost
from apps_base.promotion.models import CouponGenerate, Coupon
from apps_base.order.constants import PROCESO
from decimal import Decimal as D, getcontext


class OrderGenerate(object):

    def create(self, cart, customer, ubigeo, coupon):

        # try:
        #     shipping = ShippingCost.objects.get(ubigeo=ubigeo)
        #     price = shipping.price
        # except Exception as e:
        #     price = 0

        try:
            coupon_generate = CouponGenerate.objects.get(
                code=coupon.strip(), is_used=False, is_active=True, coupon__is_active=True)
            if coupon_generate.coupon.type_discount == 'PTJ':
                discount = (float(float(sub_total)*coupon_generate.coupon.discount) / 100)
            elif coupon_generate.coupon.type_discount == 'SLS':
                discount = coupon_generate.coupon.discount
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
            order.coupon = coupon_generate
            order.save()
        self.create_details(cart, order)
        return order

    def update(self, cart, ubigeo, coupon):
        getcontext().prec = 2
        try:
            coupon_generate = CouponGenerate.objects.get(
                code=coupon.strip(), is_used=False, is_active=True, coupon__is_active=True)
            if coupon_generate.coupon.type_discount == 'PTJ':
                discount = (float(float(sub_total)*coupon_generate.coupon.discount) / 100)
            elif coupon_generate.coupon.type_discount == 'SLS':
                discount = coupon_generate.coupon.discount
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
        if coupon_generate:
            order.coupon = coupon_generate
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