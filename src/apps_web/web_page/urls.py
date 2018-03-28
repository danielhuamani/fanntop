from django.conf.urls import url
from .views import (question, terms_conditions, payment_methods,
    pages, contact, contact_thanks, complaints_book, complaints_book_generate)

urlpatterns = [
    # url(r"^preguntas-frecuentes/$", question, name="question"),
    url(r"^contacto/$", contact, name="contact"),
    url(r"^libro-reclamaciones/$", complaints_book, name="complaints_book"),
    url(r"^contacto-gracias/$", contact_thanks, name="contact_thanks"),
    # url(r"^formas-pago/$", payment_methods, name="payment_methods"),
    url(r'^libro-reclamaciones/(?P<uuid_hash>[\w-]+)$', complaints_book_generate,
        name='complaints_book_generate'),
    url(r"^(?P<slug>[\w-]+)/$", pages, name="pages"),
]

