from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import (CoreTimeModel, CoreSeoSlugModel, CoreActiveModel, CorePositionModel)


class Category(CoreTimeModel, CoreSeoSlugModel, CoreActiveModel, CorePositionModel):
    name = models.CharField(_("Name"), max_length=255)
    image = models.ImageField(_('Photo'), upload_to='category/%Y/%m/%d')
    category = models.ForeignKey(
        "Category", related_name='category_categories', on_delete=models.SET_NULL,
        null=True, blank=True)


    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"

    def __str__(self):
        if self.category:
            return self.category.name + " - " + self.name
        else:
            return self.name
