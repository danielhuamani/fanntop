from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import CoreTimeModel, CoreActiveModel, CorePositionModel


class HomeBanner(CoreTimeModel, CoreActiveModel, CorePositionModel):
    """(HomeBanner description)"""
    name = models.CharField('Name', max_length=255)
    image = models.ImageField('Banner', upload_to='home_banner')

    def __str__(self):
        return u"HomeBanner"


class FrequentQuestion(models.Model):
    content = models.TextField(_('Content'))
    class Meta:
        verbose_name = "FrequentQuestion"
        verbose_name_plural = "FrequentQuestion"

    def __str__(self):
        return 'Question'
