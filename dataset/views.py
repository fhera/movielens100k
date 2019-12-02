import os
from datetime import datetime
from os.path import join

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView

from .forms import PeliculaBusquedaYearForm, UsuarioBusquedaForm
from .models import Categoria, Ocupacion, Pelicula, Puntuacion, Usuario

path = "data"


def index(request):
    return render(request, 'index.html')


def ingresar(request):
    if request.user.is_authenticated:
        return(HttpResponseRedirect('/populate'))
    formulario = AuthenticationForm()
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password']
        acceso = authenticate(username=usuario, password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/populate'))
            else:
                return (HttpResponse('<html><body>ERROR: USUARIO NO ACTIVO </body></html>'))
        else:
            return (HttpResponse('<html><body>ERROR: USUARIO O CONTARSE&Ntilde;A INCORRECTOS </body></html>'))

    return render(request, 'login.html', {'formulario': formulario})


class OcupacionesUsuarios(ListView):
    model = Usuario
    ordering = ['ocupacion']
    template_name = "ocupaciones_usuarios.html"


class MejoresPeliculas(ListView):
    model = Pelicula
    template_name = "mejores_peliculas.html"
    queryset = Pelicula.objects.annotate(
        avg_puntuacion=Avg('puntuacion__puntuacion')
    ).order_by('-avg_puntuacion')[:5]


class BusquedaPeliculas(FormView):
    template_name = "busqueda_peliculas.html"
    form_class = PeliculaBusquedaYearForm
    success_url = reverse_lazy("busqueda_peliculas")

    def form_valid(self, form):
        context = super().get_context_data()
        peliculas = None
        if self.request.POST:
            peliculas = Pelicula.objects.filter(
                fecha_estreno__year=form.cleaned_data['year']
            )
        context["pelicula_list"] = peliculas
        return self.render_to_response(context)


class PuntuacionesUsuario(FormView):
    template_name = "puntuaciones_usuario.html"
    form_class = UsuarioBusquedaForm
    success_url = reverse_lazy("puntuaciones_usuario")

    def form_valid(self, form):
        context = super().get_context_data()
        puntuaciones = None
        if self.request.POST:
            puntuaciones = Puntuacion.objects.filter(
                id_usuario=form.cleaned_data['id_usuario']
            )
        context["puntuaciones"] = puntuaciones
        return self.render_to_response(context)


class PopulateDatabase(LoginRequiredMixin, View):
    login_url = settings.LOGIN_REDIRECT_URL

    def get(self, request):
        populate_occupations()
        populate_genres()
        u = populate_users()
        m = populate_movies()
        # USAMOS LOS DICCIONARIOS DE USUARIOS Y PELICULAS PARA ACELERAR LA CARGA EN PUNTUACIONES
        populate_ratings(u, m)
        # se hace logout para obligar a login cada vez que se vaya a poblar la BD
        logout(request)
        return HttpResponseRedirect('/index.html')


def populate_occupations():
    print("Loading occupations...")
    Ocupacion.objects.all().delete()

    lista = []
    fileobj = open(join(path, "u.occupation"), "r")
    for line in fileobj.readlines():
        lista.append(Ocupacion(nombre=str(line.strip())))
    fileobj.close()
    # bulk_create hace la carga masiva para acelerar el proceso
    Ocupacion.objects.bulk_create(lista)

    print("Occupations inserted: " + str(Ocupacion.objects.count()))
    print("---------------------------------------------------------")


def populate_genres():
    print("Loading Movie Genres...")
    Categoria.objects.all().delete()

    lista = []
    fileobj = open(join(path, "u.genre"), "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 2:
            continue
        lista.append(Categoria(id_categoria=rip[1], nombre=rip[0]))
    fileobj.close()
    Categoria.objects.bulk_create(lista)

    print("Genres inserted: " + str(Categoria.objects.count()))
    print("---------------------------------------------------------")


def populate_users():
    print("Loading users...")
    Usuario.objects.all().delete()

    lista = []
    dict = {}
    fileobj = open(join(path, "u.user"), "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 5:
            continue
        u = Usuario(
            id_usuario=rip[0],
            edad=rip[1],
            sexo=rip[2],
            ocupacion=Ocupacion.objects.get(nombre=rip[3]),
            cp=rip[4]
        )
        lista.append(u)
        dict[rip[0]] = u
    fileobj.close()
    Usuario.objects.bulk_create(lista)

    print("Users inserted: " + str(Usuario.objects.count()))
    print("---------------------------------------------------------")
    return(dict)


def populate_movies():
    print("Loading movies...")
    Pelicula.objects.all().delete()

    lista_peliculas = []  # lista de peliculas
    # diccionario de categorias de cada pelicula (idPelicula y lista de categorias)
    dict_categorias = {}
    fileobj = open(join(path, "u.item"), "r")
    for line in fileobj.readlines():
        rip = line.strip().split('|')

        date = None if len(rip[2]) == 0 else datetime.strptime(
            rip[2], '%d-%b-%Y')
        lista_peliculas.append(
            Pelicula(
                id_pelicula=rip[0],
                titulo=rip[1],
                fecha_estreno=date,
                imdb_url=rip[4]
            )
        )

        lista_aux = []
        for i in range(5, len(rip)):
            if rip[i] == '1':
                lista_aux.append(Categoria.objects.get(pk=(i-5)))
        dict_categorias[int(rip[0])] = lista_aux
    fileobj.close()
    Pelicula.objects.bulk_create(lista_peliculas)

    dict = {}
    for pelicula in Pelicula.objects.all():
        pelicula.categorias.set(dict_categorias[pelicula.id_pelicula])
        dict[pelicula.id_pelicula] = pelicula

    print("Movies inserted: " + str(Pelicula.objects.count()))
    print("---------------------------------------------------------")
    return(dict)


def populate_ratings(u, m):
    print("Loading ratings...")
    Puntuacion.objects.all().delete()

    lista = []
    fileobj = open(join(path, "u.data"), "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        lista.append(
            Puntuacion(
                id_usuario=u[rip[0]],
                id_pelicula=m[int(rip[1])],
                puntuacion=rip[2]
            )
        )
    fileobj.close()
    Puntuacion.objects.bulk_create(lista)
    print("Ratings inserted: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")
