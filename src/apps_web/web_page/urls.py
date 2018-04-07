from django.conf.urls import url
from .views import (payment_methods,
    pages, contact, contact_thanks, complaints_book, complaints_book_generate, question_response,
    question_response_question)

urlpatterns = [
    # url(r"^preguntas-frecuentes/$", question, name="question"),
    url(r"^contacto/$", contact, name="contact"),
    url(r"^libro-reclamaciones/$", complaints_book, name="complaints_book"),
    url(r"^contacto-gracias/$", contact_thanks, name="contact_thanks"),
    url(r"^preguntas-frecuentes/$", question_response, name="question_response"),
    url(r"^preguntas-frecuentes/(?P<slug>[\w-]+)/$", question_response_question, name="question_response_question"),
    # url(r"^formas-pago/$", payment_methods, name="payment_methods"),
    url(r'^libro-reclamaciones/(?P<uuid_hash>[\w-]+)$', complaints_book_generate,
        name='complaints_book_generate'),
    url(r"^(?P<slug>[\w-]+)/$", pages, name="pages"),
]

