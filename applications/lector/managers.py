import datetime
from django.db import models
from django.db.models import Q, Count, Avg, Sum
from django.db.models.functions import Lower

class PrestamoManager(models.Manager):
    ''' procedimientos para prestamo '''

    def libros_promedio_edades(self):
        resultado = self.filter(libro__id='1').aggregate(promedio_edad=Avg('lector__edad'),
        suma_edad=Sum('lector__edad'))
        return resultado
        #esta consulta me trae la edad promedio y suma de edades de quienes han...
        #prestado un libro con id = 1
        #primero filtro por el libro en la tabla prestamo y luego hago el calculo...
        #con las edades de las personas que lo prestaron

    def num_libros_prestados(self):
        resultado = self.values('libro').annotate(num_prestados = Count('libro'),
        titulo = Lower('libro__titulo'),)

        for r in resultado:
            print('================')
            print(r, r['num_prestados'])

        return resultado

    #esta funcion devuelve la cantidad de veces que se ha prestado un libro
    #fue necesario utilizar la funcion values porque solo con la annotate me traia
    #los libros prestados pero individualmente, repitiendo registros, no los estaba
    #sumando, con la funcion values le especifico un parametro de agrupacion unico
    #el cual es el mismo libro para que pueda entonces contar los registros
    #y los muestre agrupados, en vez de mostrar el registro individual

    #SI EL MANAGER NO TIENE VISTA ES PORQUE SE VALIDÓ EN EL SHELL!