from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import (CoreTimeModel, CoreSeoSlugModel, CoreActiveModel, CorePositionModel)


class ProductClass(CoreSeoSlugModel):
    influencer = models.ForeignKey(
        "influencer.Influencer", related_name='influencer_product_class')
    category = models.ManyToManyField('category.Category', related_name='category_product_class')
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    is_variation = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        pass


class Product(CoreActiveModel, CoreTimeModel):
    sku = models.CharField(_('sku'), unique=True, max_length=120)
    stock = models.PositiveSmallIntegerField(_('stock'))
    price = models.PositiveSmallIntegerField(_('price'))
    product_class = models.ForeignKey('ProductClass', related_name='product_class_products')
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        pass

