from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    estado = models.BooleanField(
        default=True,
        verbose_name="Estado"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    class Meta:

        db_table = "categorias"

        verbose_name = "Categoría"

        verbose_name_plural = "Categorías"

        ordering = ["nombre"]


    def __str__(self):

        return self.nombre

class Libro(models.Model):

    titulo = models.CharField(
        max_length=200,
        verbose_name="Título"
    )

    autor = models.CharField(
        max_length=150,
        verbose_name="Autor"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    portada = models.ImageField(
    upload_to="libros/",
    blank=True,
    null=True,
    verbose_name="Portada"
    )

    anio_publicacion = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Año de publicación"
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="libros",
        verbose_name="Categoría"
    )

    disponible = models.BooleanField(
        default=True,
        verbose_name="Disponible"
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro"
    )

    class Meta:

        db_table = "libros"

        verbose_name = "Libro"

        verbose_name_plural = "Libros"

        ordering = ["titulo"]

    def __str__(self):

        return self.titulo

class Favorito(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favoritos"
    )

    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name="favoritos"
    )

    fecha_agregado = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = "favoritos"

        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"

        ordering = ["-fecha_agregado"]

        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "libro"],
                name="usuario_libro_unico"
            )
        ]

    def __str__(self):

        return f"{self.usuario.username} - {self.libro.titulo}"