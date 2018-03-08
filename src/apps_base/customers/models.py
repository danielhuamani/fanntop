from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from apps_base.custom_auth.models import User
from .constants import GENDER_CHOICES, TYPE_DOCUMENT_CHOICES


class Customer(models.Model):
    user = models.OneToOneField("custom_auth.User", related_name='user_customer')
    document = models.CharField(_("Document"), max_length=120)
    type_document = models.CharField(
        _("Type Document"), max_length=120, choices=TYPE_DOCUMENT_CHOICES)
    is_offers_news = models.BooleanField(_("offers and news"), default=False)
    terms_conditions = models.BooleanField("Terms and Conditions", default=True)
    gender = models.CharField(_("Gender"), max_length=120, choices=GENDER_CHOICES)
    phone = models.CharField(_("Phone"), max_length=120, blank=True)
    birth_date = models.DateField("Fecha Nacimiento", null=True)
    is_send_email = models.BooleanField(default=False)
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


class CustomerShippingAddress(models.Model):
    customer = models.ForeignKey(
        "Customer", related_name="customer_shipping_address"
    )
    first_name = models.CharField(_("Nombres"), max_length=255, blank=True)
    last_name = models.CharField(_("Apellidos"), max_length=255, blank=True)
    type_document = models.CharField(
        _("Type Document"), max_length=120, choices=TYPE_DOCUMENT_CHOICES)
    document = models.CharField(_("Document"), max_length=120)
    phone = models.CharField(_("Phone"), max_length=120)
    # name = models.CharField("Otra direccion", max_length=120, blank=True)
    address = models.CharField("Dirección", max_length=255)
    reference = models.CharField("Referencia", max_length=255)
    ubigeo = models.ForeignKey(
        "ubigeo.Ubigeo", related_name="zip_code_shipping_address")
    order = models.OneToOneField('order.OrderShippingAddress', blank=True, null=True,
        related_name='order_shipping_adress_customers', on_delete=models.SET_NULL)
    class Meta:
        verbose_name = "ShippingAddress"
        verbose_name_plural = "ShippingAddress"

    def __str__(self):
        return self.address