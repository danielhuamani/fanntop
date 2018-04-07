from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import CoreTimeModel, CoreActiveModel, CorePositionModel, CoreSeoSlugModel


class HomeBanner(CoreTimeModel, CoreActiveModel, CorePositionModel):
    """(HomeBanner description)"""
    name = models.CharField('Name', max_length=255)
    image = models.ImageField('Banner', upload_to='home_banner')

    def __str__(self):
        return u"HomeBanner"


class FrequentQuestionResponse(CoreTimeModel, CorePositionModel, CoreActiveModel, CoreSeoSlugModel):
    question = models.CharField(_('Question'), max_length=120)
    content = models.TextField(_('Content'))
    class Meta:
        verbose_name = "FrequentQuestion"
        verbose_name_plural = "FrequentQuestion"

    def __str__(self):
        return 'Question'


class TermsConditions(models.Model):
    content = models.TextField(_('Content'))

    class Meta:
        verbose_name = "TermsConditions"
        verbose_name_plural = "TermsConditionss"

    def __str__(self):
        return 'Termino Condiciones'


class PaymentMethods(models.Model):
    content = models.TextField(_('Content'))

    class Meta:
        verbose_name = "TermsConditions"
        verbose_name_plural = "TermsConditionss"

    def __str__(self):
        return 'PaymentMethods'


class Pages(CoreTimeModel, CoreActiveModel, CorePositionModel, CoreSeoSlugModel):
    name = models.CharField(_('Name'), max_length=120)
    description = models.TextField(_('Description'))

    class Meta:
        verbose_name = "Pages"
        verbose_name_plural = "Pagess"

    def __str__(self):
        return self.title
