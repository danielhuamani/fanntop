from django import forms
from apps_base.order.models import Order, OrderCustomer, OrderShippingAddress
from apps_base.ubigeo.models import Departamento, Provincia, Ubigeo
from apps_base.customers.models import CustomerShippingAddress
class OrderCustomerForm(forms.ModelForm):
    class Meta:
        model = OrderCustomer
        fields = ('first_name', 'last_name', 'phone', 'email', 'document', 'type_document')


class OrderShippingAddressForm(forms.ModelForm):
    # departamento = forms.CharField(max_length=20)
    # # provincia = forms.CharField(
    # #     queryset=Provincia.objects.none(),
    # #     empty_label="Seleccione Provincia")
    # provincia = forms.CharField(max_length=20)
    ubigeo = forms.ModelChoiceField(
        queryset=Ubigeo.objects.none(),
        empty_label="Seleccione Distrito")
    save_data = forms.BooleanField()
    direccion_save = forms.ModelChoiceField(
        queryset=CustomerShippingAddress.objects.none(),
        empty_label="Seleccione Dirección", label='Mis Direcciones', required=False)

    class Meta:
        model = OrderShippingAddress
        fields = ('first_name', 'last_name', 'phone', 'address',
            'reference', 'ubigeo', 'document', 'type_document')
