from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.
class Departamento(models.Model):
    Departamento = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.Departamento

class Provincia(models.Model):
    Provincia = models.CharField(max_length = 50)
    Departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.Provincia