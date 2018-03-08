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