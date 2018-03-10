from .models import Order, OrderDetail
from apps_base.order.constants import PROCESO

class OrderGenerate(object):

    def create(self, cart, customer):
        order = Order.objects.create(
            customer=customer,
            cart=cart,
            sub_total=cart.total,
            total=cart.total,
            type_status=PROCESO,
        )
        self.create_details(cart, order)
        return order

    def update(self, cart):
        order = Order.objects.get(cart__code=cart.code)
        order.sub_total = cart.total
        order.total = cart.total
        order.type_status = PROCESO
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