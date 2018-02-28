from apps_base.cart.models import Cart, CartItem
from apps_base.product.models import Product
from .constants import PENDING


class CartObject(object):
    """docstring for Cart"""
    def __init__(self, code):
        super().__init__()
        self.code = code

    def validate_code(self):
        return Cart.objects.filter(code=self.code).exists()

    def validate_sku_quantity(self, sku, quantity):
        if sku and quantity > 0:
            self.sku = sku
            self.quantity = quantity
            return True
        return False

    def validate_exist_product(self, sku):
        return CartItem.objects.filter(product__sku=sku, cart__code=self.code).exists()

    def validate_sku_quantity_product(self, sku, quantity):
        product = Product.objects.filter(sku=sku)
        if product.exists():
            quantity_max = product.first().stock
            return int(quantity_max) >= int(quantity)
        return False

    def validate_product(self, sku, quantity):
        return self.validate_sku_quantity(sku, quantity)

    def get_product(self, sku):
        return Product.objects.get(sku=sku)

    def get_cart(self):
        cart = Cart.objects.prefetch_related(
            'cart_items', 'cart_items__product', 'cart_items__product__product_product_images',
            'cart_items__product__product_class').get(code=self.code)
        return cart

    def generate_cart_item(self, sku, quantity):
        pass

    def update_cart_item(self, cart, product, sku, quantity):
        cart_item = CartItem.objects.get(
            cart__pk=cart.pk,
            product__pk=product.pk
        )
        cart_item.quantity = quantity
        cart_item.save()
        return True

    def delete_cart_item(self, sku):
        CartItem.objects.get(
            cart__code=self.code,
            product__sku=sku
        ).delete()
        return True

    def create_cart_item(self, cart, product, sku, quantity):
        cart_item = CartItem(
            quantity=int(quantity),
            cart=cart,
            product=product
        )
        cart_item.save()

    def add_cart_item(self, sku, quantity):
        # try:
        product = self.get_product(sku)
        cart = self.get_cart()
        if CartItem.objects.filter(
            cart__pk=cart.pk, product=product).exists():
            self.update_cart_item(cart, product, sku, quantity)
        else:
            self.create_cart_item(cart, product, sku, quantity)
            #cart.total = cart.update_total()
            #cart.save()

        # except Exception as e:
        #     print (str(e))
        #     status = 500
        #     mensaje = "No se pude agregar el producto al carrito"
        return True

    def create_cart(self):
        cart = Cart(status=PENDING)
        cart.save()
        self.code = cart.code
        return cart