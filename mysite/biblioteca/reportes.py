# -*- coding: utf-8 -*-
from tempfile import TemporaryFile
from xlwt import Workbook, XFStyle, Borders, Pattern, Font

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from biblioteca.models import Libro
from mysite import settings

from django.utils.encoding import smart_str


def archivo_excel(titulo, archivo_logo = 'unprg.bmp', label_resumen = [], datos_resumen = [], heads = [], color = 0x9ACD32, registros = [], nombre_archivo = 'descargar.xls'):

    book = Workbook()
    sheet1 = book.add_sheet('Hoja 01')

    #estilos de celda titulo
    fnt_titulo = Font()
    fnt_titulo.name = 'Arial'
    fnt_titulo.bold = True

    style_titulo = XFStyle()
    style_titulo.font = fnt_titulo

    #estilos de celda etiqueta resumen
    fnt_etiqueta_resumen = Font()
    fnt_etiqueta_resumen.name = 'Arial'
    fnt_etiqueta_resumen.bold = True

    style_etiqueta_resumen = XFStyle()
    style_etiqueta_resumen.font = fnt_etiqueta_resumen

    #estilos de celda datos resumen
    fnt_dato_resumen = Font()
    fnt_dato_resumen.name = 'Arial'

    style_dato_resumen = XFStyle()
    style_dato_resumen.font = fnt_dato_resumen

    #estilos de celda heads
    fnt_heads = Font()
    fnt_heads.name = 'Arial'
    fnt_heads.bold = True
    borders_heads = Borders()
    borders_heads.left = Borders.THIN
    borders_heads.right = Borders.THIN
    borders_heads.top = Borders.THIN
    borders_heads.bottom = Borders.THIN
    pattern_heads = Pattern()
    pattern_heads.pattern = Pattern.SOLID_PATTERN
    pattern_heads.pattern_fore_colour = color

    style_heads = XFStyle()
    style_heads.font = fnt_heads
    style_heads.borders = borders_heads
    style_heads.pattern = pattern_heads

    #estilos de celda registros
    fnt_registros = Font()
    fnt_registros.name = 'Arial'
    borders_registros = Borders()
    borders_registros.left = Borders.THIN
    borders_registros.right = Borders.THIN
    borders_registros.top = Borders.THIN
    borders_registros.bottom = Borders.THIN


    style_registros = XFStyle()
    style_registros.font = fnt_registros
    style_registros.borders = borders_registros
    
    
    sheet1.insert_bitmap(settings.MEDIA_ROOT + 'archivos_excel/%s' % archivo_logo, 1, 0)

    #escribir el titulo
    sheet1.write(10,0,titulo, style_titulo)

    row = 12
    col = 0
    #escribir las etiquetas del resumen
    for etiqueta in label_resumen:
        sheet1.write(row, col, etiqueta, style_etiqueta_resumen)
        row+=1

    row = 12
    col = 1
    #escribir los datos del resumen
    for dato in datos_resumen:
        sheet1.write(row, col, dato, style_dato_resumen)
        row+=1

    row+=1
    col = 0
    #escribimos los encabezados
    for head in heads:
        sheet1.write(row,col,head,style_heads)
        col+=1

    row+=1
    col=1
    n = 1
    #recorremos la lista y escribimos los datos
    for fila in registros:
        sheet1.write(row,0,n,style_registros)
        for dato in fila:
            sheet1.write(row,col,dato,style_registros)
            col+=1
        col=1
        row+=1
        n+=1

    #book.save(settings.MEDIA_ROOT + 'archivos_excel/%s' % nombre_archivo)
    book.save(TemporaryFile())

def archivo_excel1(titulo, archivo_logo = 'unprg.bmp', label_resumen = [], datos_resumen = [], heads = [], color = 0x9ACD32, registros = [], nombre_archivo = 'descargar.xls'):
    import StringIO
    output = StringIO.StringIO()
    from django.http import HttpResponse
    book = Workbook()
    sheet1 = book.add_sheet('Hoja 01')

    #estilos de celda titulo
    fnt_titulo = Font()
    fnt_titulo.name = 'Arial'
    fnt_titulo.bold = True

    style_titulo = XFStyle()
    style_titulo.font = fnt_titulo

    #estilos de celda etiqueta resumen
    fnt_etiqueta_resumen = Font()
    fnt_etiqueta_resumen.name = 'Arial'
    fnt_etiqueta_resumen.bold = True

    style_etiqueta_resumen = XFStyle()
    style_etiqueta_resumen.font = fnt_etiqueta_resumen

    #estilos de celda datos resumen
    fnt_dato_resumen = Font()
    fnt_dato_resumen.name = 'Arial'

    style_dato_resumen = XFStyle()
    style_dato_resumen.font = fnt_dato_resumen

    #estilos de celda heads
    fnt_heads = Font()
    fnt_heads.name = 'Arial'
    fnt_heads.bold = True
    borders_heads = Borders()
    borders_heads.left = Borders.THIN
    borders_heads.right = Borders.THIN
    borders_heads.top = Borders.THIN
    borders_heads.bottom = Borders.THIN
    pattern_heads = Pattern()
    pattern_heads.pattern = Pattern.SOLID_PATTERN
    pattern_heads.pattern_fore_colour = color

    style_heads = XFStyle()
    style_heads.font = fnt_heads
    style_heads.borders = borders_heads
    style_heads.pattern = pattern_heads

    #estilos de celda registros
    fnt_registros = Font()
    fnt_registros.name = 'Arial'
    borders_registros = Borders()
    borders_registros.left = Borders.THIN
    borders_registros.right = Borders.THIN
    borders_registros.top = Borders.THIN
    borders_registros.bottom = Borders.THIN


    style_registros = XFStyle()
    style_registros.font = fnt_registros
    style_registros.borders = borders_registros
    
    
    sheet1.insert_bitmap(settings.MEDIA_ROOT + 'archivos_excel/%s' % archivo_logo, 1, 0)

    #escribir el titulo
    sheet1.write(10,0,titulo, style_titulo)

    row = 12
    col = 0
    #escribir las etiquetas del resumen
    for etiqueta in label_resumen:
        sheet1.write(row, col, etiqueta, style_etiqueta_resumen)
        row+=1

    row = 12
    col = 1
    #escribir los datos del resumen
    for dato in datos_resumen:
        sheet1.write(row, col, dato, style_dato_resumen)
        row+=1

    row+=1
    col = 0
    #escribimos los encabezados
    for head in heads:
        sheet1.write(row,col,head,style_heads)
        col+=1

    row+=1
    col=1
    n = 1
    #recorremos la lista y escribimos los datos
    for fila in registros:
        sheet1.write(row,0,n,style_registros)
        for dato in fila:
            sheet1.write(row,col,dato,style_registros)
            col+=1
        col=1
        row+=1
        n+=1

    book.save(settings.MEDIA_ROOT + 'archivos_excel/%s' % nombre_archivo)
    book.save(output)
    output.seek(0)
    response = HttpResponse(content=output.getvalue(),mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=libros_excel.xls'
    return response


#def lista_libros():
libros = Libro.objects.all()
registros = []
for lib in libros:
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
archivo_excel(titulo,heads = headers, registros = registros)
