from django.contrib import admin
from .models import Attribute, AttributeOption


class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption
    extra = 0


class AttributeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeOptionInline,
    ]

admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeOption)