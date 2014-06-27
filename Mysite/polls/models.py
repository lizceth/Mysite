#coding: utf-8
from django.db import models
import  datetime
from django.utils import timezone

class Encuesta(models.Model):
    pregunta=models.CharField(max_length=200)
    fecha_pub=models.DateTimeField('dato de publicacion')
    def __unicode__(self):
        return self.pregunta

    def publicacion_reciente(self):
        return self.fecha_pub >=timezone.now() - datetime.timedelta(days=1)
    publicacion_reciente.admin_order_field='fecha_pub'
    publicacion_reciente.boolean=True
    publicacion_reciente.short_description='publicaciones recientes?'

class Eleccion(models.Model):
    encuesta=models.ForeignKey(Encuesta)
    texto_eleccion=models.CharField(max_length=200)
    votos=models.IntegerField(default =0)
    def __unicode__(self):
        return self.texto_eleccion
