from django.db import models
from django.utils.translation import ugettext_lazy as _


class Configuration(models.Model):
    name = models.CharField(_('Name Store'), max_length=120)
    email_contact = models.EmailField(_('Email Contact'))
    phone = models.CharField(_('Phone'), max_length=120)
    youtube = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    class Meta:
        verbose_name = "Configuration"
        verbose_name_plural = "Configurations"

    def __str__(self):
        return self.name
