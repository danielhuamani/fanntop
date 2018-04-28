from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import CoreActiveModel
from .constants import TYPE_DISCOUNT_CHOICES


class Coupon(CoreActiveModel):
    name = models.CharField(_('Name'), max_length=120)
    influencers = models.ManyToManyField(
        'influencer.Influencer', related_name='influencer_coupons', blank=True)
    is_limit = models.BooleanField(default=False)
    date_start = models.DateField(_('Date Start'), null=True, blank=True)
    date_end = models.DateField(_('Date End'), null=True, blank=True)
    prefix = models.CharField(_('Code Coupon'), max_length=120, unique=True)
    type_discount = models.CharField(_('Type Discount'),
        choices=TYPE_DISCOUNT_CHOICES, max_length=60)
    discount = models.FloatField(_('Discount'))
    quantity_customer = models.PositiveIntegerField(_('Use for Customer'), default=1)
    stock = models.PositiveIntegerField(_('Stock'), default=1)
    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.name


class CouponGenerate(CoreActiveModel):
    coupon = models.ForeignKey('Coupon', related_name='coupon_generates')
    code = models.CharField(_('Code'), max_length=120, unique=True)
    is_used = models.BooleanField(_('Is Used'), default=False)
    date_validated = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(
        'customers.Customer', related_name='customer_coupon_generates', blank=True, null=True)
    class Meta:
        verbose_name = "CouponGenerate"
        verbose_name_plural = "CouponGenerates"

    def __str__(self):
        return self.code
