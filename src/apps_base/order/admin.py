from django.contrib import admin
from .models import Order, OrderDetail, OrderShippingAddress, OrderCustomer
# Register your models here.

admin.site.register(OrderDetail)
admin.site.register(Order)
admin.site.register(OrderShippingAddress)
admin.site.register(OrderCustomer)