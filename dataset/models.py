from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Ocupacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Ocupación"
        verbose_name_plural = "Ocupaciones"
        ordering = ('nombre',)


class Usuario(models.Model):
    id_usuario = models.PositiveIntegerField(primary_key=True)
    edad = models.PositiveSmallIntegerField(
        verbose_name='Edad',
        help_text='Debe introducir una edad'
    )
    sexo = models.CharField(
        max_length=1,
        verbose_name='Sexo',
        help_text='Debe elegir entre M o F'
    )
    ocupacion = models.ForeignKey(
        "Ocupacion",
        on_delete=models.CASCADE
    )
    cp = models.TextField(verbose_name='Código Postal')

    def __str__(self):
        return str(self.id_usuario)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ('id_usuario',)


class Categoria(models.Model):
    id_categoria = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.id_categoria

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ('id_categoria',)


class Pelicula(models.Model):
    id_pelicula = models.PositiveIntegerField(primary_key=True)
    titulo = models.CharField(verbose_name="Título", max_length=50)
    fecha_estreno = models.DateField(
        verbose_name="Fecha de estreno",
        null=True
    )
    imdb_url = models.CharField(verbose_name="Url de IMDB", max_length=500)
    categorias = models.ManyToManyField('Categoria')
    puntuaciones = models.ManyToManyField(Usuario, through="Puntuacion")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Pelicula"
        verbose_name_plural = "Peliculas"
        ordering = ('titulo',)


class Puntuacion(models.Model):
    PUNTUACIONES = {
        (1, 'Muy mala'),
        (2, 'Mala'),
        (3, 'Regular'),
        (4, 'Buena'),
        (5, 'Muy buena'),
    }

    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    id_pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    puntuacion = models.PositiveSmallIntegerField(
        verbose_name='Puntuación',
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=PUNTUACIONES
    )


def __str__(self):
    return str(self.puntuacion)


class Meta:
    verbose_name = "Puntuación"
    verbose_name_plural = "Puntuaciones"
    ordering = ('id_pelicula', 'id_usuario',)
