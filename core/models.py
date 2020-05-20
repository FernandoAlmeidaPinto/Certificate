from django.db import models
import os

class Certificate(models.Model):

    name = models.CharField('Certificado', max_length=100)
    image = models.ImageField('imagem', upload_to='certificado')

    def __str__(self):
        return self.name

    def filename(self):
        return os.path.basename(self.image.name)

    class Meta:
        db_table = 'images'

class FormInformation(models.Model):

    event = models.CharField('Nome do Evento', max_length=100, blank=True)
    date = models.DateField('Data do Evento', blank=True)
    body = models.TextField('Corpo', blank=True)
    date_creaded = models.DateField(auto_now=True)
    plan = models.FileField('Filecsv',upload_to='planilhas', blank=True)

    def __str__(self):
        return self.event

    class Meta:
        db_table = 'Eventos'
