from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('lectores/', views.ListLectores.as_view(),name='lectores'),
    #path('prestamo/add/',views.RegistrarPrestamo.as_view(),name="prestamo-add"),
    path('prestamo/add/',views.AddPrestamo.as_view(),name="prestamo_add"),
    path('prestamo/multiple-add/',views.AddMutiplePrestamo.as_view(),name="prestamo_add_multiple"),
]