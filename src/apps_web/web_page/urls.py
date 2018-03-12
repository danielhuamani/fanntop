from django.conf.urls import url
from .views import question

urlpatterns = [
    url(r"^preguntas-frecuentes/$", question, name="question"),
]

