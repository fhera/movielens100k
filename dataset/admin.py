from django.contrib import admin

from .models import Categoria, Ocupacion, Pelicula, Puntuacion, Usuario

# Register your models here.
admin.site.register(Ocupacion)
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Pelicula)
admin.site.register(Puntuacion)
