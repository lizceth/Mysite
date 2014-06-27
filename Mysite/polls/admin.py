from django.contrib import admin
from polls.models import Encuesta, Eleccion

class EncuestaAdmin(admin.ModelAdmin):
    fieldsets=[
        (None, {'fields': ['pregunta']}),
        ('dato de informacion',{'fields': ['fecha_pub'], 'classes':['collapse']}),
]
    list_display=('pregunta', 'fecha_pub', 'publicacion_reciente')
    list_filter=['fecha_pub']
    search_fields=['pregunta']


class EleccionInline(admin.StackedInline):
    model=Eleccion
    extra=3

class EncuestaAdmin(admin.ModelAdmin):
    fieldsets=[
        (None, {'fields':['pregunta']}),
        ('datos de informacion ',{'fields':['fecha_pub'], 'classes':['collapse']}),

    ]
    inlines=[EleccionInline]


admin.site.register(Encuesta, EncuestaAdmin)
admin.site.register(Eleccion)

