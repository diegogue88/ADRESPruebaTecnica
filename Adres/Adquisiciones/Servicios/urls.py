from django.urls import path
from rest_framework import routers
from . import views
from .views import home, editarAdquisicion

urlpatterns = [
    
    path('', home, name='home'),
    path('registrarAdquisicion/', views.registrarAdquisicion),
    path('editarRegistro/<int:idRegistro>', views.editarRegistro, name='editar_registro'),
    path('editarAdquisicion/', editarAdquisicion, name='editar_adquisicion'),
    path('eliminarRegistro/<int:idRegistro>', views.eliminarRegistro, name='eliminar_registro'),
    path('lista_registros/', views.lista_registros, name='lista_registros'),
    path('ver_registro/<int:idRegistro>/', views.ver_registro, name='ver_registro'),


]