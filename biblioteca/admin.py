from django.contrib import admin
from .models import Categoria, Libro


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "estado",
        "fecha_creacion",
    )

    list_filter = (
        "estado",
    )

    search_fields = (
        "nombre",
    )

    ordering = (
        "nombre",
    )

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "titulo",
        "autor",
        "categoria",
        "anio_publicacion",
        "disponible",
    )

    list_filter = (
        "categoria",
        "disponible",
    )

    search_fields = (
        "titulo",
        "autor",
    )

    ordering = (
        "titulo",
    )