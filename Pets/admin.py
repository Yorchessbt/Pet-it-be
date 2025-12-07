from django.contrib import admin
from .models import Pet, Especie, Comentario, Solicitud


# Register your models here.

admin.site.register(Pet)
admin.site.register(Especie)
admin.site.register(Comentario)
admin.site.register(Solicitud)