from django import forms
from applications.libro.models import Libro
from .models import Prestamo

class PrestamoForm(forms.ModelForm):

    class Meta:
        model = Prestamo
        fields = ('lector','libro',)


class MultiplePrestamoForm(forms.ModelForm):

    libros = forms.ModelMultipleChoiceField(
        queryset = None, #aca generalmente va el queryset (Libro.objects...),
        #pero se quiso poner en None para enseñar como se puede hacer desde...
        #una funcion (en este caso desde __init__)
        required = True, # solicita que el campo sea requerido u obligatorio
        widget = forms.CheckboxSelectMultiple, #hace que aparezcan checkbox en
        #los registros traidos
    )
    #como no hay una relacion ManyToMany y se desea mostrar una lista de libros...
    #para no registrar de a uno por uno, se utiliza el ModelMultipleChoiceField...
    #para que cargue una lista del queryset

    class Meta:
        model = Prestamo
        fields = ('lector',)

    #la funcion __init__ se encanrga de mostrar un valor determinado en el HTML...
    #siempre que se muestre
    def __init__(self, *args, **kwargs):
        super(MultiplePrestamoForm, self).__init__(*args, **kwargs)
        self.fields['libros'].queryset = Libro.objects.all()
        #se inicializa la variable libros, pero como es un form se hace atraves de...
        #el atributo fields, luego se establece el queryset el cual podria ir...
        #sin problemas en la variable queryset de la clase MultiplePrestamoForm