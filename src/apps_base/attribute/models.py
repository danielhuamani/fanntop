from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import (CoreTimeModel, CoreActiveModel, CorePositionModel)
from .constants import TYPE_ATRIBUTE, INPUT, SELECT_SINGLE, SELECT_MULTIPLE
from uuslug import uuslug


class Attribute(CoreTimeModel, CoreActiveModel):
    name = models.CharField(_('Name'), max_length=255)
    name_store = models.CharField(
        _('Name Store'), max_length=255, blank=True)
    is_use_search = models.BooleanField(
        _('Use in search'), default=False)
    type_name = models.CharField(_('Type of attribute'),
        max_length=120, choices=TYPE_ATRIBUTE)
    is_filter = models.BooleanField(_('Filtered'), default=False)
    is_variation = models.BooleanField(_('Variation'), default=False)
    slug = models.CharField(max_length=120, blank=True)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Attribute, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Atributo"
        verbose_name_plural = "Atributos"
        unique_together = (('name', 'type_name'),)

    def __str__(self):
        return self.name

    # def get_type_name_value(self):
    #     self.type_name


class AttributeOption(CoreTimeModel, CoreActiveModel, CorePositionModel):
    attribute = models.ForeignKey('Attribute', related_name='attribute_options')
    attr = models.CharField(_('attr'), max_length=255, blank=True)
    option = models.CharField(_('Option'), max_length=255)
    slug = models.CharField(max_length=120)

    class Meta:
        verbose_name = "Atributo"
        verbose_name_plural = "Atributos"
        ordering = ['position']

    def __str__(self):
        return self.option


    def save(self, *args, **kwargs):
        self.slug = uuslug(self.option, instance=self, slug_field='slug', filter_dict=None)
        super(AttributeOption, self).save(*args, **kwargs)