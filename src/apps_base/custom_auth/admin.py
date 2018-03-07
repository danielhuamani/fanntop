from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class UserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ['email']
    ordering = ['email']
    readonly_fields = ['date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'type_user', 'is_active',
            'date_joined', 'last_login')}),
        ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    exclude = ()

admin.site.register(User, UserAdmin)
