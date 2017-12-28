from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuslug import uuslug


class CoreTimeModel(models.Model):
    """ Modelo Base"""
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class CoreActiveModel(models.Model):
    """Modelo Activo"""
    is_active = models.BooleanField(_('is active'), default=True)
    is_trash = models.BooleanField(_('is trash'), default=False)

    class Meta:
        abstract = True


class CorePositionModel(models.Model):
    """Modelo Posicion"""
    position = models.IntegerField(_('Position'), default=1)

    class Meta:
        verbose_name = "CorePositionModel"
        verbose_name_plural = "CorePositionModels"
        abstract = True
        ordering = ['position']


class CoreSeoUrllModel(models.Model):
    url = models.CharField(max_length=120)

    class Meta:
        verbose_name = "CoreSeoUrllModel"
        verbose_name_plural = "CoreSeoUrllModel"
        abstract = True

    def save(self, *args, **kwargs):
        if self.url:
            self.url = uuslug(self.url, instance=self, slug_field='url', filter_dict=None)
        super(CoreSeoUrllModel, self).save(*args, **kwargs)
