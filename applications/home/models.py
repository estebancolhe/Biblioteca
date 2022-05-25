from django.db import models

#un metadato es todo aquello que dentro del modelo, no es un atributo...
#o campo de la base de datos

class Persona(models.Model):
    '''Model definition for persona'''

    full_name = models.CharField('nombres', max_length=50)
    pais = models.CharField('Pais', max_length=30)
    pasaporte = models.CharField('Pasaporte', max_length=50)
    edad = models.IntegerField()
    apelativo = models.CharField('Apelativo', max_length=10)

    class Meta:
        '''Meta definition for Persona.'''

        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        db_table = 'persona'
        unique_together = ['pais','apelativo']
        #el unique_together es para indicar que no quiero un registro en la BD,
        #que tenga el mismo pais y apelativo en este caso

        #se pueden hacer pequeñas validaciones en los metadatos, en este caso
        #se validará que no se puedan registrar menores de 18 años con la ayuda del constraints
        #el name es la salida para la clase que estan invocando
        #el "gte" es para determinar que la edad sea "menor que"
        constraints = [
            models.CheckConstraint(check=models.Q(edad__gte=18), name='edad_mayor_18')
        ]
        #en esta ocasion es necesario que se creen las tablas de empleado y cliente
        #y como tienen casi los mismos atributos, es necesario que no se cree la
        #tabla persona, solo la de empleados y clientes que heredan todo de persona
        #en ocasiones es necesario que los modelos no se creen como tablas en la BD (ESTE CASO)
        #es por esto que utilizamos el abstract, de esta manera django entiende
        #que la clase persona es un modelo pero no se creará en BD
        abstract = True

    def __str__(self):
        '''Unicode representation of Persona.'''
        return self.full_name

class Empleados(Persona):
    empleo = models.CharField('Empleo', max_length=50)

class Clientes(Persona):
    email = models.EmailField('Email')#sale un error con el constraints cuando mas de...
    #un modelo hereda de persona, se comenta la clase cliente para...
    #no tener el error