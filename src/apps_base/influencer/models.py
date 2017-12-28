from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import (CoreTimeModel, CoreSeoUrllModel, CoreActiveModel, CorePositionModel)


class Influencer(CoreTimeModel, CoreActiveModel, CorePositionModel, CoreSeoUrllModel):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(_('Photo'), upload_to='influencer/%Y/%m/%d')

    title = models.CharField(_("title"), max_length=120)
    meta_description = models.CharField(_('description'), max_length=255,
                                        blank=True)
    class Meta:
        verbose_name = "Influencer"
        verbose_name_plural = "Influencers"

    def __str__(self):
        return self.name


class InfluencerSeo(CoreSeoUrllModel):
    influencer = models.OneToOneField('Influencer', related_name='influencer_influencerseo')
    title = models.CharField(_("title"), max_length=120)
    meta_description = models.CharField(_('description'), max_length=255,
                                        blank=True)
    class Meta:
        verbose_name = "InfluencerSeo"
        verbose_name_plural = "InfluencerSeos"

    def __str__(self):
        return self.title
