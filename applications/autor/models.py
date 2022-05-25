from django.db import models

#se importa el managers
from .managers import AutorManager

class Persona(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=20)
    edad = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id) + '-' + self.nombres + '-' + self.apellidos

    class Meta:
        abstract = True

class Autor(Persona):
    seudonimo = models.CharField('seudonimo', max_length=50, blank=True)
    objects = AutorManager() #de esta forma es como conectamos el managers.py con el modelo...
    #en la app de autor
