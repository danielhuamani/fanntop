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


class CoreSeoSlugModel(models.Model):
    slug = models.CharField(max_length=120)
    title = models.CharField(_("title"), max_length=120)
    meta_description = models.CharField(_('description'), max_length=255,
                                        blank=True)
    class Meta:
        verbose_name = "CoreSeoSlugModel"
        verbose_name_plural = "CoreSeoSlugModel"
        abstract = True

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = uuslug(self.slug, instance=self, slug_field='slug', filter_dict=None)
        super(CoreSeoSlugModel, self).save(*args, **kwargs)
