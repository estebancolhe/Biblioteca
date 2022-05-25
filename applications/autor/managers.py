#el archivo managers.py es para que en vez de que se hagan consultas a la BD...
#desde las views, se haga desde el managers.py
from django.db import models
from django.db.models import Q

class AutorManager(models.Manager):
    ''' managers para el modelo autor '''

    def buscar_autor(self, kword):
        resultado = self.filter(nombre__icontains=kword) #con __icontains busco coincidencias en la barra...
        #de buscar y no solo valores exactos
        return resultado

    def buscar_autor2(self, kword):#con Q es como la sentencia or en BD SQL
        resultado = self.filter(Q(nombre__icontains=kword)| Q(apellidos__icontains=kword))
        return resultado

    def buscar_autor3(self, kword):#exclude es para excluir las busquedas dependiendo de la condicion
        resultado = self.filter(nombre__icontains=kword).exclude(Q(edad__icontains=69) | Q(edad__icontains=1001))
        return resultado

    def buscar_autor4(self, kword):#esto es para hacer condicion and en BD SQL, solo se necesita...
        #separar por coma(,) y poner la otra condicion
        #con order_by ordeno dependiendo del campo que especifique
        resultado = self.filter(edad__gt=90, edad__lt=1002).order_by('apellidos', 'nombre', 'id')
        return resultado


    #def listar_autores(self):
        
        #return self.all() #como se va a utilizar este manager exclusivamente para el modelo...
        #autor entonces no es necesario en la consulta hacer el Autor.objects.all() en las vistas...
        #solo es necesario hacer el Autor.objects.listar_autores()...
        #ya que la funcion listar_autores() se encarga de retornar self.all()...
        #que retorna todos los datos guardados en la tabla autores