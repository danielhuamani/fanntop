from django import forms
from apps_base.custom_auth.models import User
from apps_base.order.models import Order, OrderCustomer
from apps_base.customers.models import Customer, CustomerShippingAddress
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from apps_base.ubigeo.models import Ubigeo

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('document', 'type_document', 'gender', 'phone')



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')



class CustomerShippingAddressForm(forms.ModelForm):
    ubigeo = forms.ModelChoiceField(
        queryset=Ubigeo.objects.none(),
        empty_label="Seleccione Distrito")
    class Meta:
        model = CustomerShippingAddress
        fields = ('first_name', 'last_name', 'type_document', 'document',
            'phone', 'address', 'reference', 'ubigeo')


class FollowOrdersForm(forms.Form):
    email = forms.EmailField()
    num_order = forms.CharField(max_length=120)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('cleaned_data')
    #     num_order = cleaned_data.get('cleaned_data')
    #     order = Order.objects.get(code=num_order, order_order_customer__email=email)
