from django.db import models
from applications.libro.models import Libro
from applications.autor.models import Persona
from .managers import PrestamoManager
from django.db.models.signals import post_delete

class Lector(Persona):
    
    class Meta:
        verbose_name = 'Lector'
        verbose_name_plural = 'Lectores'

class Prestamo(models.Model):
    lector = models.ForeignKey(Lector,on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro,on_delete=models.CASCADE, related_name='libro_prestamo')
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)
    devuelto = models.BooleanField()

    objects = PrestamoManager()

    #logica desde los modelos para disminuir la cant. de libros disponibles en el campo stock
    def save(self, *args, **kwargs):
        self.libro.stock = self.libro.stock - 1
        self.libro.save()

        super(Prestamo, self).save(*args, **kwargs)

    def __str__(self):
        return self.libro.titulo


def update_libro_stock(sender, instance, **kwargs):
    # actualizamos el stock cuando se elimina un prestamo
    instance.libro.stock = instance.libro.stock + 1
    instance.libro.save()

post_delete.connect(update_libro_stock, sender=Prestamo)