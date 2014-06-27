from django.conf.urls import patterns, url
from  polls import views

urlpatterns =patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^especificos/(?P<pk_id>\d+)/$', views.DetalleView.as_view(), name='detalle'),
    url(r'^(?P<encuesta_id>\d+)/voto/$', views.voto, name='voto'),
    url(r'^(?P<pk_id>\d+)/resultado/$', views.ResultadoView.as_view(), name='resultado'),
)
