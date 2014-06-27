# coding:utf-8
from django.contrib import admin
from ubicacion.models import Departamento, Provincia

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('Departamento',)
    search_fields = ['Departamento',]

admin.site.register(Departamento,DepartamentoAdmin)

class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('Provincia', 'Departamento',)
    search_fields = ['Provincia',]

admin.site.register(Provincia,ProvinciaAdmin)

