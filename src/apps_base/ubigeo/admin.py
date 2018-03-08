from django.contrib import admin
from .models import Ubigeo, Departamento, Provincia
# Register your models here.
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ['cod_prov', 'desc_prov']

admin.site.register(Ubigeo)
admin.site.register(Departamento)
admin.site.register(Provincia, ProvinciaAdmin)
