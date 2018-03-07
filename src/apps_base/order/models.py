from django.db import models
from .constants import TYPE_STATUS
from .utils import generate_code_order
from apps_base.customers.constants import TYPE_DOCUMENT_CHOICES
from apps_base.core.models import CoreTimeModel, CoreActiveModel

class Order(CoreTimeModel, CoreActiveModel):
    customer = models.ForeignKey(
        'customers.Customer', related_name="customer_orders")
    cart = models.OneToOneField(
        'cart.Cart', related_name="cart_order", null=True, blank=True
    )
    code = models.CharField("code", max_length=255, unique=True)
    sub_total = models.DecimalField("sub total", decimal_places=2, max_digits=8)
    shipping_price = models.DecimalField("Envio", decimal_places=2, max_digits=8)
    total = models.DecimalField("total", decimal_places=2, max_digits=8)
    type_status = models.CharField(
        "type_status", choices=TYPE_STATUS, max_length=255, blank=True)
    is_send_email = models.BooleanField(default=False)
    is_return_stock = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Order"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code_order()
        super(Cart, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.code)



class OrderDetail(models.Model):
    order = models.ForeignKey(
        "Order", related_name="order_orderdetail"
    )
    productdetail = models.ForeignKey(
        'product.Product', related_name="product_orderdetails"
    )
    quantity = models.IntegerField()
    price = models.DecimalField("price", decimal_places=2, max_digits=8)
    sub_total = models.DecimalField("sub_total", default=0, decimal_places=2, max_digits=8)
    total = models.DecimalField("total", decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = "OrderDetail"
        verbose_name_plural = "OrderDetail"
        unique_together = ('order', 'productdetail',)


class OrderCustomer(models.Model):
    order = models.OneToOneField(
        "Order", related_name="order_order_customer"
    )
    first_name = models.CharField("Apellido Paterno", max_length=255)
    last_name = models.CharField("Apellido Materno", max_length=255)
    email = models.EmailField("Email")
    phone = models.CharField("Celular", max_length=120)
    document = models.CharField("Documento", blank=True, max_length=120)
    type_document = models.CharField(
        "Tipo Documento", blank=True, choices=TYPE_DOCUMENT_CHOICES, max_length=120)

    class Meta:
        verbose_name = "OrderCustomer"
        verbose_name_plural = "OrderCustomer"

    def get_full_name(self):
        return "{0} {1} {2}".format(self.name, self.first_name, self.last_name)


class OrderShippingAddress(models.Model):
    order = models.OneToOneField(
        "Order", related_name="order_ordershipping"
    )
    first_name = models.CharField("Apellido Paterno", blank=True, max_length=255)
    last_name = models.CharField("Apellido Materno", blank=True, max_length=255)
    address = models.CharField("Dirección", max_length=255)
    reference = models.CharField("Referencia", max_length=255)
    ubigeo = models.ForeignKey("ubigeo.Ubigeo", related_name='ubigeo_order_shipping_address')
    document = models.CharField("Documento", blank=True, max_length=120)
    type_document = models.CharField(
        "Tipo Documento", blank=True, choices=TYPE_DOCUMENT_CHOICES, max_length=120)
    phone = models.CharField("Celular", max_length=120)
    shipping_address = models.ForeignKey("customers.CustomerShippingAddress", null=True, blank=True)

    class Meta:
        verbose_name = "OrderShipping"
        verbose_name_plural = "OrderShipping"