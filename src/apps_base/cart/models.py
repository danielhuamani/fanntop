from decimal import Decimal as D
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import (CoreTimeModel, CoreSeoSlugModel, CoreActiveModel, CorePositionModel)
from .constants import CART_STATUS_CHOICES
from .utils import generate_code


class Cart(CoreTimeModel):
    code = models.CharField(_("Cart Code"), unique=True, max_length=120)
    user = models.ForeignKey('custom_auth.User', related_name='user_carts', null=True, blank=True)
    status = models.CharField(_('Status'), choices=CART_STATUS_CHOICES, max_length=120)
    extra_data = JSONField(default={}, blank=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
        super(Cart, self).save(*args, **kwargs)


    @property
    def total(self):
        total = D(0)
        for cart_item in self.cart_items.all().select_related('product'):
            total += cart_item.cart_item_total
        return total
        # return self.cart_items.all().annotate(total=models.F('cart_items__quantity') * models.F('cart_items__product__quantity'))

    def __str__(self):
        return self.code


class CartItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    cart = models.ForeignKey('Cart', related_name='cart_items')
    product = models.ForeignKey('product.Product', related_name='product_cart_items')
    extra_data = JSONField(default={}, blank=True)

    class Meta:
        verbose_name = "CartItem"
        verbose_name_plural = "CartItems"
        unique_together = ('product', 'cart')
        ordering = ('id',)

    def __str__(self):
        return '{0}{1}'.format(self.cart.code, self.product.sku)

    @property
    def cart_item_total(self):
        return D(self.quantity * self.product.get_price)