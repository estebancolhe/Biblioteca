import datetime
from django.db import models
from django.db.models import Q, Count
from django.contrib.postgres.search import TrigramSimilarity

class LibroManager(models.Manager):
    ''' managers para el modelo libro '''

    def listar_libros(self, kword):
        resultado = self.filter(titulo__icontains=kword)
        return resultado

#con los trigram hago busquedas como las hace google, es decir, asi escriba la palabra mal...
#u omita letras, ejm, quiero buscar "astronauta" y escribo "astrnata"...
#los trigrams empiezan a hacer combinaciones de esas palabras para traerme un resultado...
#una de las palabras que se pueden conformar con esas letras es "astronauta" y...
#es uno de los resultados que traerá la busqueda
#NOTA: como es una triagramacion, la busqueda debe tener al menos...
#3 caracteres
    def listar_libros_trg(self, kword):

        if kword:
            resultado = self.filter(titulo__trigram_similar=kword)
            return resultado
        else:
            return self.all()[:10]
            #despues del all(), los corchetes[:10] significa que la consulta
            #muestre los 10 primeros registros

    def listar_libros2(self, kword, fecha1, fecha2):
        date1 = datetime.datetime.strptime(fecha1, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(fecha2, "%Y-%m-%d").date()

        resultado = self.filter(titulo__icontains=kword, fecha__range=(date1, date2))
        return resultado

    def listar_libros_categorias(self, categoria):

        return self.filter(categoria__id=categoria).order_by('titulo')

    def add_autor_libro(self, libro_id, autor):
        libro = self.get(id=libro_id)
        libro.autores.add(autor)
        return libro

    def libros_num_prestamos(self):
        resultado = self.aggregate(
            num_prestamos = Count('libro_prestamo')
        )
        #esta consulta muestra la cantidad de prestamos realizados
        return resultado

        #diferencia entre aggregate y annotate...
        #annotate devuelve una consulta queryset y añadido a la consulta la operacion...
        # aritmetica que se esté realizando, en este caso es Count()...
        #aggregate devuelve un diccionario de valores en vez de un queryset y añadido al diccionario...
        #la operacion aritmetica que se esté realizando, en este caso Count()

        #se utiliza annotate para un conteo (cuantos libros hay por categoria)...
        #se utiliza aggregate cuando se utiliza una operacion artimetica...
        # para encontrar un valor

    def num_libros_prestados(self):
        resultado = self.annotate(num_prestados = Count('libro_prestamo'))

        for r in resultado:
            print('================')
            print(r, r.num_prestados)

        return resultado
    
class CategoriaManager(models.Manager):
    '''managers para el modelo autor'''

    #este manager me trae las categorias dependiendo del autor que busque gracias al related_name...
    #el cual es categoria_libro
    def categoria_por_autor(self, autor):
        return self.filter(categoria_libro__autores__id=autor).distinct() 
        #este manager se probó con el manage.py shell por eso no tiene url ni template
        
        #el distinct() hace que me raiga informacion sin repetir, asi la informacion...
        #esté varias veces

    def listar_categoria_libros(self):
        resultado = self.annotate(
            num_libros = Count('categoria_libro')
        )
        #esta consulta trae la cantidad de libros que hay por categoria
        for r in resultado:
            print('*******')
            print(r,r.num_libros)
        return resultado
        #funcion annotate permite devolver datos de varios modelos en un solo registro
        #este manager se probó con el python manage.py shell...
        #se importó los modelos (from applications.libro.models import *)...
        #y se ejecutó el manager (Categoria.objects.listar_categoria_libros())