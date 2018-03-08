from django.shortcuts import render
from django.http import JsonResponse
from .models import Departamento, Provincia, Ubigeo


def departamentos(request):
    data = {'departamentos': []}
    for departamento in Departamento.objects.order_by('desc_dep'):
        data['departamentos'].append({
            'codigo': departamento.cod_dep,
            'descripcion': departamento.desc_dep
        })
    return JsonResponse(data)


def provincias(request):
    data = {'provincias': []}
    departamento = request.GET.get('departamento', '01')
    for provincia in Provincia.objects.filter(cod_prov__startswith=departamento).order_by('desc_prov'):
        data['provincias'].append({
            'codigo': provincia.cod_prov,
            'descripcion': provincia.desc_prov
        })
    return JsonResponse(data)


def distritos(request):
    data = {'distritos': []}
    provincia = request.GET.get('provincia')
    for distrito in Ubigeo.objects.filter(cod_ubigeo_inei__startswith=provincia).order_by('desc_ubigeo_inei'):
        data['distritos'].append({
            'pk': distrito.pk,
            'descripcion': distrito.desc_ubigeo_inei
        })
    return JsonResponse(data)
