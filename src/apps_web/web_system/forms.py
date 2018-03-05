from django import forms
from apps_base.custom_auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

