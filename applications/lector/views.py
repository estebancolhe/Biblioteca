from django.shortcuts import render
from datetime import date
from django.views.generic import ListView
from applications.lector.managers import PrestamoManager
from .models import Lector
from django.views.generic.edit import FormView
from .models import Prestamo
from .forms import PrestamoForm, MultiplePrestamoForm
from django.http import HttpResponseRedirect

class ListLectores(ListView):
    context_object_name = 'lista_lectores'
    template_name = 'lector/lista.html'

    def get_queryset(self):
        return Lector.objects.all()

#Realizar un prestamo sencillo de un libro 
class RegistrarPrestamo(FormView):
    template_name = 'lector/add_prestamo.html'
    form_class = PrestamoForm
    success_url = '.' # se redirecciona a la misma vista con el '.'

    def form_valid(self, form):

        #otra forma de registrar informacion
        '''Prestamo.objects.create(
            lector=form.cleaned_data['lector'],
            libro=form.cleaned_data['libro'],
            #con el cleaned_data['campo'], es con lo que recuperamos el valor del campo que se
            #establece desde el formulario y se asigna a una variable en este caso libro y lector
            fecha_prestamo=date.today(),
            devuelto=False
        )'''
        
        prestamo = Prestamo(
            lector=form.cleaned_data['lector'],
            libro=form.cleaned_data['libro'],
            fecha_prestamo=date.today(),
            devuelto=False
        )
        prestamo.save()
        #la diferencia entre .create y .save es que .create crea desde 0...
        #mientras que .save crea desde 0, pero si el registro ya existe...
        #solo lo actualiza

        #logica (dese las vistas) para disminuir la cant. de libros disponibles en el campo stock
        libro = form.cleaned_data['libro'] #form.cleaned_data captura la informacion enviada...
        #desde el HTML
        libro.stock = libro.stock - 1
        libro.save()

        return super(RegistrarPrestamo, self).form_valid(form)


#realizar un prestamo de un libro con la validacion de que si no existe el prestamo
#al usuario que lo solicita que lo realice y 
# si ya existe el prestamo al mismo usuario que indique que ya existe un prestamo 
class AddPrestamo(FormView):
    template_name = 'lector/add_prestamo.html'
    form_class = PrestamoForm
    success_url = '.'

    def form_valid(self, form):

        #el metodo get_or_create utiliza dos variables, obj es para guardar el objeto...
        #o recuperarlo y create es un booleano para ver si fue almacenado o no

        #el get_or_create en este caso esta haciendo la validacion con los campos de...
        #lector (quien presta el libro) y libro (libro a prestar) y el booleano...
        #devuelto para saber si el lector devolvio el libro o no al momento de solicitarlo...
        #prestado
        obj , create = Prestamo.objects.get_or_create(
            lector = form.cleaned_data['lector'],
            libro = form.cleaned_data['libro'],
            devuelto = False,
            defaults={
                'fecha_prestamo':date.today()
            }
        )

        if create:
            return super(AddPrestamo, self).form_valid(form)
        else:
            return HttpResponseRedirect('/')


class AddMutiplePrestamo(FormView):
    template_name = 'lector/add_multiple_prestamo.html'
    form_class = MultiplePrestamoForm
    success_url = '.'

    def form_valid(self, form):

        prestamos = []
        for l in form.cleaned_data['libros']:
            prestamo = Prestamo(
                lector = form.cleaned_data['lector'],
                libro = l,
                fecha_prestamo = date.today(),
                devuelto = False
            )#recien con este codigo se creo un objeto "prestamo" con el formato
            #que solicita el modelo "Prestamo"

            prestamos.append(prestamo) #si fuera del for se pone el .save()...
            #se guardan los libros cada vez que se itera el objeto...
            #(form.cleaned_data['libros']), esto no es optimo, por eso...
            #se crea una lista "prestamos" y se agrega cada objeto...
            # de la lista iterable (form.cleaned_data['libros']) a esa lista para...
            #despues guardar todo de una sola vez con la ayuda del atributo...
            #bulk_create('nombre de la lista a guardar')

        Prestamo.objects.bulk_create(prestamos)#con bulk_create() guardo una lista...
        #con multiples datos, asi creo varios prestamos de una sola vez

        return super(AddMutiplePrestamo, self).form_valid(form)