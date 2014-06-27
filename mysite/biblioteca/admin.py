# -*- coding: utf-8 -*-
from django.contrib import admin
from biblioteca.models import Libro
from biblioteca.models import Autor
from biblioteca.models import CategoriaLibro
from biblioteca.models import DetalleLibro
from biblioteca.models import Prestamo
from biblioteca.models import Usuario
from ubicacion.models import Departamento, Provincia
from django import forms
from django.forms.util import ErrorList
from biblioteca.widgets import DateTimeWidget
from mysite import settings

class DetalleLibroInline(admin.TabularInline):
    model = DetalleLibro

class CategoriaLibroAdmin(admin.ModelAdmin):
    list_display = ('Nombre',)
admin.site.register(CategoriaLibro, CategoriaLibroAdmin)

class AutorAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ['Nombres','Apellidos',]
admin.site.register(Autor, AutorAdmin)

class LibroAdmin(admin.ModelAdmin):
    list_display = ('Codigo','Titulo','Autores','Cantidad','Disponibles','CategoriaLibro','FechaIngreso',)
    list_filter = ('CategoriaLibro',)
    search_fields = ['Codigo','Titulo','Autor__Apellidos','Autor__Nombres']
    filter_horizontal = ('Autor',)
    inlines = [
        DetalleLibroInline,
    ]
    actions = ['libros_xls']

    def libros_xls(self, request, queryset):
        from biblioteca.reportes import archivo_excel1
        from django.utils.encoding import smart_str
        registros = []
	for lib in queryset:
            codigo = lib.Codigo
	    titulo = unicode(lib.Titulo)
	    autores = unicode(lib.Autores())
	    categoria = unicode(lib.CategoriaLibro)
	    fecha = lib.FechaIngreso.strftime("%d-%m-%Y")
	    cantidad = lib.Cantidad()
	    disponibles = lib.Disponibles()
	    registros.append([codigo, titulo, autores, categoria, fecha, cantidad, disponibles])
    
        headers = ['N',u'Código',u'Título','Autores',u'Categoría','Fecha Ingreso', 'Cantidad', 'Disponibles']
        titulo = 'LIBROS'
        return archivo_excel1(titulo,heads = headers, registros = registros)
    libros_xls.short_description = "Descargar xls"
admin.site.register(Libro, LibroAdmin)

class DetalleLibroAdmin(admin.ModelAdmin):
    list_display = ('Codigo','Titulo','SubCodigo','Autor','Anio','Edicion','Tomo','FechaIngreso',)
    search_fields = ['Libro__Titulo','Libro__Codigo',]
    raw_id_fields = ("Libro",)
admin.site.register(DetalleLibro, DetalleLibroAdmin)

class PrestamoAdminForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data = self.cleaned_data
        usuario = cleaned_data.get("Usuario")

        if usuario == "":
            msg = u"Debes Ingresar un Usuario"
            self._errors["Usuario"] = ErrorList([msg])
            del cleaned_data["Usuario"]
        else:
        # Only do something if both fields are valid so far.
            prestamos = Prestamo.objects.filter(Usuario = usuario,Entregado = True, Devuelto = False)
            if prestamos.count() != 0:
                msg = u"El Usuario ya tiene libros prestados."
                self._errors["Usuario"] = ErrorList([msg])
                del cleaned_data["Usuario"]
        
        # Always return the full collection of cleaned data.
        return cleaned_data

    class Meta:
        model = Prestamo

class PrestamoAdmin(admin.ModelAdmin):
    form = PrestamoAdminForm
    list_display = ('Username','NombreUsuario','CodigoLibro','DetalleLibro','Prestamo','Vencimiento','Entregado','Devuelto','Entrega',)
    search_fields = ['Usuario__Nombres','Usuario__ApellidoPaterno','Usuario__ApellidoMaterno','DetalleLibro__Libro__Codigo','DetalleLibro__Libro__Titulo']
    raw_id_fields = ("DetalleLibro","Usuario",)
    list_filter = ('Prestamo','Entregado','Devuelto',)
admin.site.register(Prestamo, PrestamoAdmin)

class UsuarioAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UsuarioAdminForm, self).__init__(*args, **kwargs)
	try:
	    self.fields['selected_dep'].initial = self.instance.Provincia.Departamento.id
            self.fields['selected_prov'].initial = self.instance.Provincia.id
        except:
            pass

    #Nacimiento = forms.DateField(widget = DateTimeWidget)
    Departamento = forms.ModelChoiceField(queryset = Departamento.objects.all().order_by('Departamento'), widget = forms.Select(), required = False)
    selected_dep = forms.CharField(widget = forms.HiddenInput, required = False,label = "")
    selected_prov = forms.CharField(widget = forms.HiddenInput, required = False,label = "")

    class Meta:
        model = Usuario

    class Media:
        js = (settings.STATIC_URL + "admin/js/jquery.min.js",
	      settings.STATIC_URL + "custom/js/Usuarios/frmusuario.js",
	      settings.STATIC_URL + "custom/calendario_admin/src/js/jscal2.js",
	      settings.STATIC_URL + "custom/calendario_admin/src/js/lang/es.js"
	     )
	
	css = {
	       "all": (settings.STATIC_URL + "custom/calendario_admin/src/css/jscal2.css",
	       settings.STATIC_URL + "custom/calendario_admin/src/css/border-radius.css",
	       settings.STATIC_URL + "custom/calendario_admin/src/css/reduce-spacing.css",
	       settings.STATIC_URL + "custom/calendario_admin/src/css/steel/steel.css",)
	       }


class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm
    list_per_page = 30
    list_display = ('Username','__unicode__',)

    fieldsets = (
        ('Datos del Usuario', {
            'fields': (('ApellidoPaterno','ApellidoMaterno','Nombres'),('Nacimiento','Sexo'),'Foto',('Departamento','Provincia','Distrito'),('Direccion','Email'),'Observaciones','Estado','selected_dep','selected_prov',),
        }),
    )
    search_fields = ('Nombres', 'ApellidoPaterno','ApellidoMaterno',)
    radio_fields = { "Sexo": admin.HORIZONTAL}
    list_filter = ('Estado',)
    
admin.site.register(Usuario, UsuarioAdmin)
