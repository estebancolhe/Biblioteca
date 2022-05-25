from django.shortcuts import render
from django.views.generic import ListView
from .models import Autor

class ListAutores(ListView):
    context_object_name = 'lista_autores'
    template_name = 'autor/lista.html'

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')

        return Autor.objects.buscar_autor4(palabra_clave)
        #return Autor.objects.listar_autores() #como ya se conectó el managers.py con el models.py...
        #de autores entonces envez de utilizar Autor.objects.all() para traer todos los registros...
        #se utiliza el Autor.objects.listar_autores(), donde listar_autores() es la funcion de...
        #managers.py que returna todos los registros con el self.all()