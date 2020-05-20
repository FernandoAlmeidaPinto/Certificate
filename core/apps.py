import os
import textwrap
import smtplib

from django.apps import AppConfig
from django.conf import settings

from PIL import Image, ImageDraw, ImageFont

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class CoreConfig(AppConfig):
    name = 'core'

class CreateCertificate:

    def PreviewCretificate(self, image, data, evento, body):
        self.path = settings.MEDIA_STATIC
        self.image = image
        self.data = data
        self.evento = evento
        self.body = body
        self.path_original = os.path.join(settings.MEDIA_ROOT, self.image)
        self.path_save = os.path.join(self.path, 'certificado.png')

        for _, _, files in os.walk(self.path):
            if files != []:
                os.remove(self.path_save)
        #Onde meu arquivo Original se encontra
        
        im = Image.open(self.path_original)
        draw = ImageDraw.Draw(im)
        
        font = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
            , 30
            )
        font2 = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
            , 30
            )
        draw.text((115,380), self.data, (0,0,0), font=font
            )
        draw.text((310,520), self.evento, (0,0,0), font=font
        )
        para = textwrap.wrap(body, width=50)
        L, H = im.size
        current_h, pad = 230, 20
        for line in para:
            l, h = draw.textsize(line, font=font)
            draw.text(((L-l)/2,current_h), line, (0,0,0), font=font2)
            current_h += h + pad

        #Onde eu quero Salvar
        
        im.save(self.path_save)

    def SendEmail(self, nome, email):
        self.nome = nome
        self.email = email
        fromaddr = 'fernando.almeida.pinto@gmail.com'
        toaddr =  self.email
        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = 'Certicidado Evento'

        body = '\nCertificado do evento'

        msg.attach(MIMEText(body, 'plain'))

        file = os.path.join(settings.MEDIA_STATIC, 'certificado.png')
        im = Image.open(file)
        L, _ = im.size
        draw = ImageDraw.Draw(im)
        
        font = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
            , 30
            )
        l, _ = draw.textsize(self.nome, font=font)
        draw.text(((L-l)/2,145), nome, (0,0,0), font=font)
        im.save(os.path.join(settings.MEDIA_STATIC, 'certificado_temp.png'))
        filename = os.path.join(settings.MEDIA_STATIC, 'certificado_temp.png')

        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        attachment.close()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, 'Ab.87226905')
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print('\nEmail enviado com sucesso')
    
    def remove(self):
        self.path = settings.MEDIA_STATIC
        for _, _, files in os.walk(self.path):
            if files != []:
                os.remove(os.path.join(self.path, files[0]))
