from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django import forms
from django.utils.translation import ugettext_lazy as _
from apps_base.custom_auth.models import User
from apps_base.custom_auth.constants import ADMIN

class AuthenticationSuperAdminForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=username, type_user=ADMIN)
        except User.DoesNotExist:
            raise forms.ValidationError(_("this email is not registered"))

        return super().clean()