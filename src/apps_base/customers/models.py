from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from apps_base.custom_auth.models import User
from .constants import GENDER_CHOICES, TIPO_DOCUMENTO_CHOICES


class Customer(models.Model):
    user = models.OneToOneField("custom_auth.User", related_name='user_customer')
    document = models.CharField(_("Document"), max_length=120)
    type_document = models.CharField(
        _("Type Document"), max_length=120, choices=TIPO_DOCUMENTO_CHOICES)
    is_offers_news = models.BooleanField(_("offers and news"), default=False)
    terms_conditions = models.BooleanField("Terms and Conditions", default=True)
    gender = models.CharField(_("Gender"), max_length=120, choices=GENDER_CHOICES)
    phone = models.CharField(_("Phone"), max_length=120, blank=True)
    birth_date = models.DateField("Fecha Nacimiento", null=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.user.email

# Create your models here.
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
