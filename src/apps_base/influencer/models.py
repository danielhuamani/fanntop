from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import (CoreTimeModel, CoreSeoSlugModel, CoreActiveModel, CorePositionModel)


class Influencer(CoreTimeModel, CoreActiveModel, CorePositionModel, CoreSeoSlugModel):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(_('Photo'), upload_to='influencer/%Y/%m/%d')


    class Meta:
        verbose_name = "Influencer"
        verbose_name_plural = "Influencers"

    def __str__(self):
        return self.name
