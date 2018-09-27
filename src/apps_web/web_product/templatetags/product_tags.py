from django import template

register = template.Library()

@register.filter(name='chunks')
def chunks(ls, dv=2):
    listado = [ls[i * dv:(i + 1) * dv] for i in range((len(ls) + dv - 1) // dv )]
    return listado

@register.filter(name='parse_list')
def parse_list(ls):
    return list(ls)