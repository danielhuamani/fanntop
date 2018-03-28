from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps_base.core.models import CoreTimeModel, CoreActiveModel
from apps_base.customers.constants import GENDER_CHOICES, TYPE_DOCUMENT_CHOICES
from .constants import TYPE_CLAIM_CHOICES, WELL_CONTRACTED_CHOICES
import uuid


class Suscription(CoreTimeModel, CoreActiveModel):
    email = models.EmailField(_('Email'), unique=True)

    class Meta:
        verbose_name = "Suscription"
        verbose_name_plural = "Suscriptions"

    def __str__(self):
        return self.email


class Contact(CoreTimeModel):
    first_name = models.CharField(_('First Name'), max_length=120)
    last_name = models.CharField(_('Last Name'), max_length=120)
    email = models.EmailField(_('Email'), max_length=120)
    phone = models.CharField(_('Celephone'), max_length=120)
    subject = models.CharField(_('Subject'), max_length=120)
    message = models.TextField(_('Message'))

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.first_name


class ComplaintsBook(CoreTimeModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(_('First Name'), max_length=120)
    last_name = models.CharField(_('Last Name'), max_length=120)
    email = models.EmailField(_('Email'), max_length=120)
    document = models.CharField(_("Document"), max_length=120)
    type_document = models.CharField(
        _("Type Document"), max_length=120, choices=TYPE_DOCUMENT_CHOICES)
    phone = models.CharField(_('Celephone'), max_length=120)
    ubigeo = models.ForeignKey('ubigeo.Ubigeo', related_name='ubigeo_complaints_book')
    address = models.CharField(_('Address'), max_length=250)
    type_claim = models.CharField(_('Type Claim'), max_length=5, choices=TYPE_CLAIM_CHOICES)
    detail = models.TextField()
    pedido = models.CharField(max_length=120, blank=True)
    well_contracted = models.CharField(max_length=120, choices=WELL_CONTRACTED_CHOICES)
    desciption = models.TextField()
    mount = models.PositiveIntegerField(null=True, blank=True)
    consumers_order = models.TextField()
    observation = models.TextField(blank=True)
    class Meta:
        verbose_name = "ComplaintsBook"
        verbose_name_plural = "ComplaintsBook"

    def __str__(self):
        return self.email
