# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from biblioteca.models import CategoriaLibro, Libro, DetalleLibro
#imports para la paginacion
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import RequestContext

from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate
from django import forms
from django.forms.util import ErrorList

def busqueda(request):
    query = request.GET.get('q','')
    query1 = request.GET.get('c', '')
    
    categorias = CategoriaLibro.objects.all()
    
    results = Libro.objects.all()

    if query1:
        results1 = results.filter(CategoriaLibro__id = query1)
    else:
        results1 = results
    
    if query:
        qset = (
            Q(Autor__Nombres__icontains = query)|
            Q(Autor__Apellidos__icontains = query)|
            Q(Titulo__icontains = query)|
            Q(Codigo__icontains = query)
        )
        results2 = results1.filter(qset).distinct()
    else:
        results2 = results1.all()

    n_libros = results2.count()
    paginator = Paginator(results2, 100)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        results = paginator.page(page)
    except (EmptyPage, InvalidPage):
        results = paginator.page(paginator.num_pages)
    
    return render_to_response("libros/busqueda.html", {"results": results,"query": query,"query1": query1,"categorias": categorias,"n_libros": n_libros,"paginator": paginator }, context_instance = RequestContext(request))

def detallelibro(request,id_libro):
    try:
        DatosLibro = Libro.objects.get(id = id_libro)
        results = DetalleLibro.objects.filter(Libro=id_libro)
    except:
        results = []
    return render_to_response("libros/detallelibro.html", {"results": results,"DatosLibro": DatosLibro }, context_instance = RequestContext(request))
    
    
class LoginForm(forms.Form):
    Usuario = forms.CharField(label = "Usuario",required = True)
    Password = forms.CharField(widget=forms.PasswordInput, label = "Contraseña",required = True)
    Libro = forms.CharField(widget=forms.HiddenInput, label = "",required = True)
     
    def clean(self):
        cleaned_data = self.cleaned_data
        user = cleaned_data.get("Usuario")
        passwd = cleaned_data.get("Password")
        libro = cleaned_data.get("Libro")

        if user and passwd and libro :
            try:
                usuario_udl = User.objects.get(username = user)
                if usuario_udl.check_password(passwd) == False:
                    msg = u'Contraseña incorrecta'
                    self._errors["Password"] = ErrorList([msg])
                    del cleaned_data["Password"]
            except User.DoesNotExist:
                msg = u'Usuario Incorrecto'
                self._errors["Usuario"] = ErrorList([msg])
                del cleaned_data["Usuario"]
            
            try:
                libro = DetalleLibro.objects.get(id = libro)
            except DetalleLibro.DoesNotExist:
                msg = u'Libro Incorrecto'
                self._errors["Usuario"] = ErrorList([msg])
                del cleaned_data["Usuario"]            
            
        return cleaned_data

@csrf_protect
@never_cache
def login_prestamo_libros(request, id_detallelibro):
    if request.method == 'POST':
         form = LoginForm(request.POST)
         if form.is_valid():
	     usuario = form.cleaned_data['Usuario']
	     passwd = form.cleaned_data['Password']
	     libro = form.cleaned_data.get("Libro")
	     libro = DetalleLibro.objects.get(id = libro)
             user = authenticate(username = usuario, password = passwd)
             if user is not None:
                 return render_to_response("libros/prestamo_satisfactorio.html", {"usuario": usuario, "libro": libro }, context_instance = RequestContext(request))
    else:
	form = LoginForm(initial = { "Libro": id_detallelibro } )

    return render_to_response("libros/login_prestamo_libros.html", {"form": form }, context_instance = RequestContext(request))