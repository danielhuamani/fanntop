from django.utils.translation import ugettext_lazy as _

PENDING = _('PENDING')
CHECKOUT = _('CHECKOUT')
ORDER = _('ORDER')
INACTIVE = _('INACTIVE')
CART_STATUS_CHOICES = (
    (INACTIVE, _('Inactive')),
    (PENDING,  _('Pending')),
    (CHECKOUT,  _('Checkout')),
    (ORDER,  _('Order'))
)