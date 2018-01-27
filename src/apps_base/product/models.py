from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import (CoreTimeModel, CoreSeoSlugModel, CoreActiveModel, CorePositionModel)


class ProductClass(CoreSeoSlugModel):
    influencer = models.ForeignKey(
        "influencer.Influencer", related_name='influencer_product_class')
    category = models.ManyToManyField('category.Category', related_name='category_product_class')
    family = models.ManyToManyField('family.Family', related_name='family_product_class')
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    is_variation = models.BooleanField(default=False)
    attribute = models.ManyToManyField('attribute.Attribute', related_name='attribute_product_class')
    
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


class ProductAttributeValue(models.Model):

    attribute = models.ForeignKey(
        'attribute.Attribute',
        on_delete=models.CASCADE,
        related_name="attribute_product_attr_value",
        verbose_name=_("Attribute"))
    product = models.ForeignKey(
        'ProductClass',
        on_delete=models.CASCADE,
        related_name='product_class_product_attr_value',
        verbose_name=_("Product"))

    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_boolean = models.NullBooleanField(_('Boolean'), blank=True)
    value_input = models.CharField(_('Input'), blank=True, max_length=255)
    value_multi_option = models.ManyToManyField(
        'attribute.AttributeOption', blank=True,
        related_name='attr_option_product_attr_multi_value',
        verbose_name=_("Value multi option"))
    value_option = models.ForeignKey(
        'attribute.AttributeOption',
        blank=True,
        null=True,
        related_name="attr_option_product_attr_value",
        on_delete=models.CASCADE,
        verbose_name=_("Value option"))
