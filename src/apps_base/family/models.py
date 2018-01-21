from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import (CoreTimeModel, CoreActiveModel, CorePositionModel)


class Family(CoreTimeModel, CoreActiveModel):

    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        verbose_name = "Family"
        verbose_name_plural = "Familys"

    def __str__(self):
        return self.name


class FamilyGroup(CorePositionModel):
    name = models.CharField(_('Name'), max_length=255)
    family = models.ForeignKey(
        "Family", related_name='family_familygroup',
        null=True, blank=True)

    class Meta:
        verbose_name = "FamilyGroup"
        verbose_name_plural = "FamilyGroups"

    def __str__(self):
        return self.name


class FamilyGroupAttribute(CoreTimeModel, CoreActiveModel, CorePositionModel):
    family_group = models.ForeignKey(
        "FamilyGroup", related_name='familygroup_familygroupatribute',
        null=True, blank=True)
    atribute = models.ForeignKey(
        "attribute.Attribute", related_name='attribute_familygroupatribute',
        null=True, blank=True)
    is_required = models.BooleanField(
        'Obligatorio', default=False)

    class Meta:
        verbose_name = "Family Group Atribute"
        verbose_name_plural = "Family Group Atribute"

    def __str__(self):
        return self.name if self.name else '-'




