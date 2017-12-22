from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import(
    LoginView,
)
from .forms import AuthenticationSuperAdminForm


def admistrador(request):
    context = {}
    return render(request, "administrador/index.html", context)


class LoginAdminView(LoginView):
    """docstring for LoginAdminView"""
    form_class = AuthenticationSuperAdminForm
    template_name = "administrador/login.html"
    success_url = reverse_lazy("administrador:administrador_login")

    def get_success_url(self):
        return reverse_lazy("administrador:admistrador")

def login_admistrador(request):
    context = {}
    return render(request, "administrador/login.html", context)