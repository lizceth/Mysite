from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from polls.models import Encuesta, Eleccion
from django.views import generic
from django.core.urlresolvers import reverse
def index(request):
    ultima_lista=Encuesta.objects.all().order_by('fecha_pub')[:5]
    context={'ultima_lista':ultima_lista}
    return render(request, 'polls/index.html', context)
    #template=loader.get_template('polls/index.html')

def detalle(request, encuesta_id):
    encuesta=get_object_or_404(Encuesta, pk=encuesta_id)
    return render(request, 'polls/detalle.html', {'encuesta':encuesta})

def resultado (request, encuesta_id):
    encuesta=get_object_or_404(Encuesta, pk=encuesta_id)
    return render(request, 'polls/resultado.html', {'encuesta':encuesta})

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='ultima_lista'
    def get_queryset(self):
        return Encuesta.objects.order_by ('fecha_pub')[:5]

class DetalleView(generic.DetailView):
    model=Encuesta
    template_name='polls/detalle.html'

class ResultadoView(generic.DetailView):
    #poll=get_object_or_404(Poll, pk=poll_id)
    #return render (request, 'polls/results.html',{'poll':poll})
    model=Encuesta
    template_name='polls/resultado.html'

def voto(request, encuesta_id):
    p=get_object_or_404(Encuesta, pk=encuesta_id)
    try:
        seleccionar=p.eleccion_set.get(pk=request.POST['eleccion'])
    except (KeyError, Eleccion.DoesNotExist):
        return render(request, 'polls/detalle.html', {
        'encuesta':p,
        'error_message':"No ha seleccionado ninguna opcion.",
        })
    else:
        seleccionar.votos +=1
        seleccionar.save()
        return HttpResponseRedirect (reverse('encuestas:resultado', args=(p.id,)))

