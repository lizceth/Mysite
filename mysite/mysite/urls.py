from django.conf.urls import patterns, include, url
from biblioteca.views import busqueda, detallelibro, login_prestamo_libros
from ubicacion.views import provincia

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', busqueda),
    url(r'ver_detalle/(\d{1,4})/$', detallelibro),
    url(r'login/(\d+)/$', login_prestamo_libros),
    url(r'provincias/(?P<departamento_id>\d*)/$', provincia, name='provincia'),
    url(r'^admin/', include(admin.site.urls)),
)
