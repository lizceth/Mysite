# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from ubicacion.models import Provincia

ESTADO_CHOICES = (
    ('Disponible', 'Disponible'),
    ('Prestado', 'Prestado'),
)

GENDER_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)

class CategoriaLibro(models.Model):
    Nombre = models.CharField(max_length = 50,unique = True)

    def __unicode__(self):
        return u'%s' % self.Nombre

    class Meta:
        verbose_name = "Categoría de Libro"
        verbose_name_plural = "Categorías de Libros"

class Autor(models.Model):
    Nombres = models.CharField(max_length=50)
    Apellidos = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s %s' % (self.Nombres, self.Apellidos)

    class Meta:
        verbose_name = "Autor de Libro"
        verbose_name_plural = "Autores de Libro"
        unique_together = (("Nombres", "Apellidos"),)

class Libro(models.Model):
    Codigo = models.CharField("Código", max_length = 4, unique = True)
    Titulo = models.CharField("Título", max_length = 100)
    Autor = models.ManyToManyField(Autor, verbose_name = "Autor(es)")
    CategoriaLibro = models.ForeignKey(CategoriaLibro, verbose_name = "Categoría")
    ImagenLibro = models.ImageField(upload_to="ImagenesLibros/%Y/%m/%d",null = True, blank = True, verbose_name = "Imágen")
    Sinopsis = models.TextField(null = True, blank = True)
    FechaIngreso = models.DateField(editable = False,verbose_name="Fecha de Ingreso", auto_now_add = True)

    def __unicode__(self):
        return u'%s %s' % (self.Codigo,self.Titulo)

    def Autores(self):
	cadena = ""
        for campo in self.Autor.all():
	    cadena += campo.__unicode__() + ', '
	return cadena

    def Cantidad(self):
        return self.detallelibro_set.count()

    def Disponibles(self):
        consulta = self.detallelibro_set.filter(Estado = 'Disponible')
        return consulta.count()

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

class DetalleLibro(models.Model):
    SubCodigo = models.CharField("SubCódigo",max_length = 4, unique = True)
    Libro = models.ForeignKey(Libro)
    ArchivoLibro = models.FileField(upload_to = "LibrosDigitales/%Y/%m/%d", null = True, blank = True, verbose_name = "Archivo de Libro")
    Editorial = models.CharField(max_length = 100,null = True, blank = True)
    Anio = models.CharField("Año",max_length = 4,null = True,blank = True)
    Edicion = models.CharField("Edición",max_length = 10,null = True,blank = True)
    Tomo = models.CharField("Tomo/Volumen",max_length = 5,null = True,blank = True)
    Estado = models.CharField("Estado",max_length = 20, choices = ESTADO_CHOICES, default = 'Disponible')
    Comentario = models.TextField(null = True, blank = True)
    FechaIngreso = models.DateField(editable = False,verbose_name="Fecha de Ingreso", auto_now_add = True)

    def __unicode__(self):
        return u'%s %s' % (self.SubCodigo,self.Libro.Titulo)

    def Codigo(self):
        return u'%s' % self.Libro.Codigo

    def Titulo(self):
        return u'%s' % (self.Libro.Titulo)

    def Categoria(self):
        return self.Libro.CategoriaLibro

    def Autor(self):
        cadena = ""
        for campo in self.Libro.Autor.all():
         cadena += str(campo) + ', '
        return cadena

    class Meta:
      verbose_name = "Ejemplar de Libro"
      verbose_name_plural = "Ejemplares de Libro"

class Usuario(User):
    Nombres = models.CharField(max_length = 100)
    ApellidoPaterno = models.CharField("Ape. Pat.",max_length = 100)
    ApellidoMaterno = models.CharField("Ape. Mat.",max_length = 100)
    Nacimiento = models.DateField()
    Sexo = models.CharField(max_length = 1,choices = GENDER_CHOICES)
    Provincia = models.ForeignKey(Provincia)
    Distrito = models.CharField(max_length = 50)
    Direccion = models.CharField("Dirección",max_length=100)
    Email = models.EmailField("E-mail", null=True, blank=True)
    Observaciones = models.TextField(blank=True, null=True)
    Estado = models.BooleanField("Activado",default = True)
    
    def obtenerpath(instance, filename):
        return u'usuarios/%s/%s' % (instance.username, filename)
    
    Foto = models.ImageField(upload_to = obtenerpath,blank=True, null=True, verbose_name = "Foto")

    def __unicode__(self):
        return u'%s %s %s' % (self.ApellidoPaterno, self.ApellidoMaterno, self.Nombres)

    def Username(self):
        return self.username
    
    def Departamento(self):
        return self.Provincia.Departamento
    
    def save(self):
	import random
        if not self.user_ptr_id:
	    self.username = self.Nombres[0].lower() + self.ApellidoPaterno.lower()
	    self.first_name = self.Nombres
	    self.last_name = self.ApellidoPaterno + " " + self.ApellidoMaterno
	    self.email = self.Email
	    contrasena = self.username
	    self.set_password(contrasena)
            super(Usuario, self).save()
        else:
	    self.first_name = self.Nombres
	    self.last_name = self.ApellidoPaterno + " " +  self.ApellidoMaterno
	    self.email = self.Email
            return super(Usuario, self).save()
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Prestamo(models.Model):
    Usuario = models.ForeignKey(Usuario)
    DetalleLibro = models.ForeignKey(DetalleLibro, verbose_name = "Libro")
    Prestamo = models.DateField(verbose_name = "Fecha Préstamo")
    Vencimiento = models.DateField(verbose_name = "Fecha Vencimiento")
    Entregado = models.BooleanField(verbose_name = "Entregado")
    Devuelto = models.BooleanField(verbose_name = "Devuelto")
    Entrega = models.DateField(null = True, blank = True,verbose_name = "Fecha Entrega")

    def __unicode__(self):
        return u'%s - %s' % (self.Usuario,self.DetalleLibro)
    
    def Username(self):
        return self.Usuario.username

    Username.short_description = "Usuario"

    def NombreUsuario(self):
        return u'%s %s' % (self.Usuario.first_name,self.Usuario.last_name)
    
    NombreUsuario.short_description = "Apellidos y Nombres"
    
    def CodigoLibro(self):
        return u'%s' % self.DetalleLibro.Libro.Codigo
    
    CodigoLibro.short_description = "Código"

    def save(self):
        if self.Entregado == True and self.Devuelto == True:
            self.DetalleLibro.Estado = 'Disponible'
        elif self.Entregado == True and self.Devuelto == False:
            self.DetalleLibro.Estado = 'Prestado'
        elif self.Entregado == False and self.Devuelto == True:
            self.DetalleLibro.Estado = 'Disponible'
            self.Devuelto = False
        else:
            self.DetalleLibro.Estado = 'Disponible'
        self.DetalleLibro.save()
        return super(Prestamo, self).save()

    class Meta:
      verbose_name = "Préstamo de Libro"
      verbose_name_plural = "Préstamos de Libros"
