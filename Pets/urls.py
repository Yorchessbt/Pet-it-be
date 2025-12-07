from django.urls import path
from Pets.views import *
from Perfil.views import *

from . import views

urlpatterns = [
    path('informacion/', views.informacion, name='informacion'),
    path('adopt_me/<int:pk>/', adopt_me, name='adopt_me'),
    path('pets/', views.pets, name='pets'),
    path('add_pet/', add_pet, name='add_pet'),
    path('search/', views.search, name='search'),
    path('edit_pet/<int:pk>/', views.edit_pet, name='edit_pet'),
    path('solicitud/<int:pk>/', views.solicitudes, name='solicitudes'),
    path('bandeja/', views.bandeja, name='bandeja'),
    path('mis-respuestas/', views.bandeja_respuesta, name='bandeja_respuesta'),
    path('respuesta/<int:pk>/', views.respuesta, name='respuesta'),
]
