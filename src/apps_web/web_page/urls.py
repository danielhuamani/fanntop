from django.conf.urls import url
from .views import question, terms_conditions, payment_methods, pages

urlpatterns = [
    # url(r"^preguntas-frecuentes/$", question, name="question"),
    # url(r"^terminos-condiciones/$", terms_conditions, name="terms"),
    # url(r"^formas-pago/$", payment_methods, name="payment_methods"),
    url(r"^(?P<slug>[\w-]+)/$", pages, name="pages"),
]


