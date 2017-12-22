from django.conf.urls import url
from .views import admistrador, LoginAdminView

urlpatterns = [
    url(r"^administrador/$", admistrador, name="admistrador"),
    url(r"^administrador/login/$", LoginAdminView.as_view(), name="administrador_login")
]

