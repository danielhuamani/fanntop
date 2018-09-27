from django.utils.translation import ugettext_lazy as _

GENDER_CHOICES = (
    ("M", _("Male")),
    ("F", _("Female"))
)

TYPE_DOCUMENT_CHOICES = (
    ("DNI", "DNI"),
    ("CE", "Carnet de extranjería")
)

TYPE_ADDRESS_CHOICES = (
    ("CASA", "Casa"),
    ("OFICINA", "Oficina"),
    ("DEPARTAMENTO", "Departamento"),
    ("CASA_PLAYA", "Casa de playa"),
    ("CASA_CAMPO", "Casa de campo"),
    ("OTRO", "Otro")
)