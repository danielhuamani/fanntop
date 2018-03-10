from django.contrib import admin
from .models import Customer, CustomerShippingAddress

admin.site.register(Customer)
admin.site.register(CustomerShippingAddress)
# Register your models here.
