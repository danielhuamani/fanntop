import smtplib

# Define to/from
sender = 'mix.minds@gmail.com'
recipient = 'danielhuamani15@gmail.com'

# server = smtplib.SMTP('smtp.zoho.com', 587)
# server.starttls()
# server.login(sender, 'fanntop$2553736')
# msg = "YOUR MESSAGE!"
# print('enates')
# server.sendmail(sender, recipient, msg)
# print('envio')
# server.quit()

# import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
fromaddr = sender
toaddr = recipient
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Subject"
body = "Write your message here"
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(sender, 'pueblolibre2')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()