from uuid import uuid4
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from django.conf import settings

def send_mail_order_success(order):
    htmly = get_template('mailing/order_success.html')
    c_d = {}
    # c_d['url_site'] = settings.URL_SITE
    # c_d['fecha_agenda'] = fecha_agenda
    c_d['order'] = order
    c_d['URL_SITE'] = settings.URL_SITE
    c_d['order_details'] = order.order_orderdetail.all(
        ).prefetch_related('productdetail', 'productdetail__product_class')
    # c_d["cliente_token"] = cliente_token
    # c_d['content_email'] = content_email
    # c_d['descripcion'] = descripcion
    html_content = htmly.render(c_d)
    asunto = u'Recibimos tu orden de compra'
    mail = u'Fanntop <%s>' % (settings.DEFAULT_FROM_EMAIL)
    # emails_destino = info.email_form.split(',')
    msg = EmailMessage(
        asunto, html_content, mail,
        [order.order_order_customer.email, 'danielhuamani15@gmail.com'])
    msg.content_subtype = "html"
    # msg.send()
    try:
        msg.send()
        order.is_send_email = True
        order.save()
    except:
        pass