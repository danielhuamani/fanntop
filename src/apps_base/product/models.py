from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.attribute.constants import INPUT, SELECT_SINGLE
from apps_base.core.models import (CoreTimeModel, CoreSeoSlugModel, CoreActiveModel, CorePositionModel)
from .utils import generate_sku
from .contants import PROCESS_CHOICES


class ProductClass(CoreSeoSlugModel, CoreActiveModel):
    influencer = models.ForeignKey(
        "influencer.Influencer", related_name='influencer_product_class')
    category = models.ManyToManyField('category.Category', related_name='category_product_class')
    family = models.ForeignKey('family.Family', related_name='family_fk_product_class', null=True)
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    characteristics = models.TextField(_('characteristics'))
    is_variation = models.BooleanField(default=False)
    attribute = models.ManyToManyField('attribute.Attribute', related_name='attribute_product_class', blank=True)
    is_published = models.BooleanField(default=False)
    data_sheet = JSONField(default={})
    price = models.DecimalField(_('price'), default=0, decimal_places=2, max_digits=5)
    process = models.CharField(max_length=120, choices=PROCESS_CHOICES)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products Class"

    def __str__(self):
        return self.name

    def get_influencer_name(self):
        return self.influencer.name


class Product(CoreActiveModel, CoreTimeModel):
    sku = models.CharField(_('sku'), unique=True, max_length=120)
    stock = models.PositiveSmallIntegerField(_('stock'), default=0)
    price = models.DecimalField(_('price'), default=0, decimal_places=2, max_digits=5)
    product_class = models.ForeignKey('ProductClass', related_name='product_class_products')
    is_featured = models.BooleanField(default=False)
    attribute_option = models.ManyToManyField('attribute.AttributeOption', related_name='attribute_product_option', blank=True)
    is_variation = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        # unique_together = ('attribute_option', 'product_class')

    def __str__(self):
        return self.sku

    @property
    def is_exhausted(self):
        if self.is_active:
            return self.stock <= 0
        return True

    def get_image(self):
        try:
            return self.product_product_images.order_by('-is_featured').first().product_image.image
        except Exception as e:
            return ''

    @property
    def get_price(self):
        return self.price

    def save(self, *args, **kwargs):
        if self.is_featured:
            Product.objects.filter(product_class=self.product_class).exclude(id=self.id).update(is_featured=False)
        if not self.sku:
            self.sku = generate_sku()
        super(Product, self).save(*args, **kwargs)


class ProductGaleryImage(models.Model):
    image = models.ImageField(upload_to='product/%Y/%m/%d/')
    name = models.CharField(_('Name'), max_length=255, blank=True)
    product_class = models.ForeignKey('ProductClass', related_name='product_class_galery_images')

    class Meta:
        verbose_name = "ProductGaleryImage"
        verbose_name_plural = "ProductGaleryImages"

    def __str__(self):
        return 'Galery'


class ProductAttributeValue(models.Model):

    attribute = models.ForeignKey(
        'attribute.Attribute',
        on_delete=models.CASCADE,
        related_name="attribute_product_attr_value",
        verbose_name=_("Attribute"))
    product_class = models.ForeignKey(
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

    class Meta:
        verbose_name = "ProductAttributeValue"
        verbose_name_plural = "ProductAttributeValues"
        unique_together = ('attribute', 'product_class')

    def __str__(self):
        return 'Product Atribute'

    def get_value(self):
        attr = self.attribute.type_name
        if attr == INPUT:
           return self.value_input
        elif attr == SELECT_SINGLE:
            return self.value_option.option
        return ''


class ProductImage(CorePositionModel):
    is_featured = models.BooleanField(default=False)
    product_image = models.ForeignKey('ProductGaleryImage', related_name='product_galery_images')
    product = models.ForeignKey('Product', related_name='product_product_images')

    class Meta:
        verbose_name = "ProductImages"
        verbose_name_plural = "ProductImagess"

    def __str__(self):
        return 'Product Image'

    def save(self, *args, **kwargs):
        if self.is_featured:
            ProductImage.objects.filter(product=self.product).exclude(id=self.id).update(is_featured=False)
        else:
            product_image = ProductImage.objects.filter(product=self.product)
            if not product_image.filter(is_featured=True).exists() and product_image.exists():
                product_image.first().is_featured = True
                product_image.save()
        super(ProductImage, self).save(*args, **kwargs)
