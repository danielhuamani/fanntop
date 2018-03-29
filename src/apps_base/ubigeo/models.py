from django.db import models

class Departamento(models.Model):
    cod_dep = models.CharField('Código', max_length=2, blank=True, null=True, db_index=True)
    desc_dep = models.CharField('Descripción', max_length=13, blank=True, null=True)

    def __str__(self):
        return self.desc_dep


class Provincia(models.Model):
    cod_prov = models.CharField('Código', max_length=4, blank=True, null=True, db_index=True)
    desc_prov = models.CharField('Descripción', max_length=25, blank=True, null=True)

    def __str__(self):
        return self.desc_prov


class Ubigeo(models.Model):
    cod_dep_inei = models.CharField(max_length=2, blank=True, null=True)
    desc_dep_inei = models.CharField(max_length=13, blank=True, null=True)
    cod_prov_inei = models.CharField(max_length=4, blank=True, null=True)
    desc_prov_inei = models.CharField(max_length=25, blank=True, null=True)
    cod_ubigeo_inei = models.CharField(primary_key=True, max_length=6, db_index=True)
    desc_ubigeo_inei = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        verbose_name = "Ubigeo"
        verbose_name_plural = "Ubigeo"


    def __str__(self):
        return self.desc_ubigeo_inei

    def full_ubigeo(self):
        return '{} / {} / {}'.format(self.desc_dep_inei, self.desc_prov_inei, self.desc_ubigeo_inei, )
