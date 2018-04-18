from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from .constants import TYPE_STATUS, TYPE_STATUS_SHIPPING, ALMACEN
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
    shipping_price = models.DecimalField("Envio", decimal_places=2, max_digits=8, default=0)
    discount = models.DecimalField("Descuento", decimal_places=2, max_digits=8, default=0)
    # coupon = models.OneToOneField('promotion.CouponGenerate', related_name='coupon_order', blank=True, null=True)
    coupon_discount = models.ForeignKey('promotion.Coupon', related_name='coupon_orders', blank=True, null=True)
    total = models.DecimalField("total", decimal_places=2, max_digits=8)
    type_status = models.CharField(
        "type_status", choices=TYPE_STATUS, max_length=255, blank=True)
    type_status_shipping = models.CharField(
        "type status shipping", choices=TYPE_STATUS_SHIPPING, max_length=255, default=ALMACEN)
    is_send_email = models.BooleanField(default=False)
    is_return_stock = models.BooleanField(default=False)
    extra_data = JSONField(default={}, blank=True)
    discount_stock = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Order"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code_order()
        super(Order, self).save(*args, **kwargs)

    def update_total(self):
        self.sub_total = self.cart.total
        self.total = self.cart.total + self.shipping_price
        self.save()

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
    first_name = models.CharField(_('Name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    email = models.EmailField("Email")
    phone = models.CharField("Celular", max_length=120, blank=True)
    document = models.CharField("Documento", blank=True, max_length=120)
    type_document = models.CharField(
        "Tipo Documento", blank=True, choices=TYPE_DOCUMENT_CHOICES, max_length=120)

    class Meta:
        verbose_name = "OrderCustomer"
        verbose_name_plural = "OrderCustomer"

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __str__(self):
        return '{}'.format(self.first_name)

class OrderShippingAddress(models.Model):
    order = models.OneToOneField(
        "Order", related_name="order_ordershipping"
    )
    first_name = models.CharField(_('Name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    address = models.CharField("Dirección", max_length=255)
    reference = models.CharField("Referencia", max_length=255, blank=True)
    ubigeo = models.ForeignKey("ubigeo.Ubigeo", related_name='ubigeo_order_shipping_address')
    document = models.CharField("Documento", blank=True, max_length=120)
    type_document = models.CharField(
        "Tipo Documento", blank=True, choices=TYPE_DOCUMENT_CHOICES, max_length=120)
    phone = models.CharField("Celular", max_length=120)
    shipping_address = models.ForeignKey("customers.CustomerShippingAddress", null=True, blank=True)

    class Meta:
        verbose_name = "OrderShipping"
        verbose_name_plural = "OrderShipping"

    def __str__(self):
        return '{}'.format(self.first_name)

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)
