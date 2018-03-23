from django import forms
from apps_base.form.models import Contact, ComplaintsBook


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone', 'subject', 'message',)


class ComplaintsBookForm(forms.ModelForm):
    class Meta:
        model = ComplaintsBook
        fields = ('first_name', 'last_name', 'email', 'document',
            'type_document', 'phone', 'ubigeo', 'address', 'type_claim',
            'detail', 'pedido', 'well_contracted', 'desciption', 'mount',
            'consumers_order', 'observation')
