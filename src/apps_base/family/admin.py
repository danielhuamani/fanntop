from django.contrib import admin
from .models import Family, FamilyGroup, FamilyAttribute
# Register your models here.

admin.site.register(Family)
admin.site.register(FamilyGroup)
admin.site.register(FamilyAttribute)
