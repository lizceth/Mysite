# Create your views here.
from django.http import HttpResponse
from django.core import serializers
from ubicacion.models import Provincia

def provincia(request, departamento_id):
    if departamento_id <> "":
      return HttpResponse(serializers.serialize('json', Provincia.objects.filter(Departamento=departamento_id), fields=('pk','Provincia')))
