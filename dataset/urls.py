from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (MejoresPeliculas, OcupacionesUsuarios, PopulateDatabase,
                    index, ingresar, BusquedaPeliculas, PuntuacionesUsuario)

urlpatterns = [
    path('populate/', PopulateDatabase.as_view(), name='populate-view'),
    path('', index, name='index-view'),
    path('index.html', index, name='index-view'),
    path('login/', ingresar, name='login-view'),
    path(
        'ocupaciones_usuarios/',
        OcupacionesUsuarios.as_view(),
        name='ocupaciones_usuarios'
    ),
    path(
        'mejores_peliculas/',
        MejoresPeliculas.as_view(),
        name='mejores_peliculas'
    ),
    path(
        'busqueda_peliculas/',
        BusquedaPeliculas.as_view(),
        name='busqueda_peliculas'
    ),
    path(
        'puntuaciones_usuario/',
        PuntuacionesUsuario.as_view(),
        name='puntuaciones_usuario'
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
