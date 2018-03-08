from uuid import uuid4
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from django.conf import settings

def send_mail_customer_welcome(user):
    print('entroooo')
    htmly = get_template('mailing/customer_welcome_email.html')
    c_d = {}
    # c_d['url_site'] = settings.URL_SITE
    # c_d['fecha_agenda'] = fecha_agenda
    c_d['user'] = user
    # c_d["cliente_token"] = cliente_token
    # c_d['content_email'] = content_email
    # c_d['descripcion'] = descripcion
    html_content = htmly.render(c_d)
    asunto = u'Registro Fanntop'
    mail = u'Fanntop <%s>' % (settings.DEFAULT_FROM_EMAIL)
    # emails_destino = info.email_form.split(',')
    msg = EmailMessage(asunto, html_content, mail, [user.email])
    msg.content_subtype = "html"
    # msg.send()
    try:
        msg.send()
        customer = user.user_customer
        customer.is_send_email = True
        customer.save()
    except:
        pass