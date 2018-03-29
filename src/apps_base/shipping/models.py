from django.db import models
from django.utils.translation import ugettext_lazy as _


class ShippingCost(models.Model):
    ubigeo = models.ForeignKey('ubigeo.Ubigeo', related_name='ubigeo_shipping_costs')
    price = models.DecimalField(
        _("Price"), decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = "ShippingPrice"
        verbose_name_plural = "ShippingPrices"

    def __str__(self):
        return str(self.price)
