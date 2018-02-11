from django.contrib import admin
from .models import Product, ProductClass, ProductImage, ProductAttributeValue


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class ProductClassAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]



admin.site.register(Product)
admin.site.register(ProductClass, ProductClassAdmin)
admin.site.register(ProductAttributeValue)
