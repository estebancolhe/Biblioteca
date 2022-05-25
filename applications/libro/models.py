from django.db import models
from .managers import LibroManager, CategoriaManager
from django.db.models.signals import post_save #signals son los triggers en django
from PIL import Image

#Se importa el modelo Autor porque en el campo autores de la tabla libro se llama...
#Ya que la relacion es de muchos a muchos  
from applications.autor.models import Autor

class Categoria(models.Model):
    nombre = models.CharField(max_length=30)

    objects = CategoriaManager()

    def __str__(self):
        return str(self.id) + ' - ' + self.nombre

class Libro(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,
    related_name='categoria_libro') #foreignkey de la tabla Categoria
    #con el foreignkey logro obtener informacion de categoria desde libro pero...
    # con el related_name logro obtener informacion de libro desde categoria ya que categoria...
    # no tiene un atributo o foreignkey de libro (libro tiene atributo de categoria)
    #cuando hago el related_name debo hacer migraciones
    autores = models.ManyToManyField(Autor) #relacion muchos a muchos
    titulo = models.CharField(max_length=50)
    fecha = models.DateField('Fecha de lanzamiento')
    portada = models.ImageField(upload_to='portada') #upload_to='portada' es la carpeta donde...
    #se almacenaran las imagenes cargadas
    visitas = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)

    objects = LibroManager()

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo', 'fecha']

    def __str__(self):
        return str(self.id) + ' - ' + self.titulo


#funcion para bajar tamaño de las portadas
def optimize_image(sender, instance, **kwargs):
    #con instance obtengo los datos del objeto creado en este caso el libro
    if instance.portada:
        portada = Image.open(instance.portada.path)#instance.portada.path es la ruta 
        #donde se guarda la portada
        portada.save(instance.portada.path, quality=20, optimize=True)#con quality bajo el peso un 20%

post_save.connect(optimize_image, sender=Libro)