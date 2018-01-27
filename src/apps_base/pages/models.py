from django.db import models
from apps_base.core.models import CoreTimeModel, CoreActiveModel, CorePositionModel


class HomeBanner(CoreTimeModel, CoreActiveModel, CorePositionModel):
    """(HomeBanner description)"""
    name = models.CharField('Name', max_length=255)
    image = models.ImageField('Banner', upload_to='home_banner')

    def __str__(self):
        return u"HomeBanner"
