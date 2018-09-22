from django import template

register = template.Library()

@register.filter(name='chunks')
def chunks(ls, dv=2):
    listado = []
    part_list = zip(*[iter(ls)]*dv)
    for x in list(part_list):
        listado.append(list(x))

    return listado

@register.filter(name='parse_list')
def parse_list(ls):
    print(ls, 'lsss')
    return list(ls)