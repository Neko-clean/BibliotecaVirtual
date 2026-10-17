from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Categoria, Libro, Favorito
from .forms import CategoriaForm, LibroForm

def categorias(request):

    if request.method == "POST":

        form = CategoriaForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('categorias')

    else:

        form = CategoriaForm()

    categorias = Categoria.objects.all()

    context = {

        'categorias': categorias,
        'form': form

    }

    return render(
        request,
        'biblioteca/categorias.html',
        context
    )


def editar_categoria(request, id):

    categoria = get_object_or_404(
        Categoria,
        id=id
    )

    if request.method == "POST":

        form = CategoriaForm(
            request.POST,
            instance=categoria
        )

        if form.is_valid():

            form.save()

            return redirect(
                'categorias'
            )

    else:

        form = CategoriaForm(
            instance=categoria
        )

    categorias = Categoria.objects.all()

    return render(
        request,
        'biblioteca/categorias.html',
        {
            'categorias': categorias,
            'form': form,
            'editando': True,
            'categoria': categoria
        }
    )

def libros(request, id=None):

    # EDITAR LIBRO
    if id:

        libro = get_object_or_404(
            Libro,
            id=id
        )

        if request.method == "POST":

            form = LibroForm(
                request.POST,
                request.FILES,
                instance=libro
            )

            if form.is_valid():

                form.save()

                return redirect('libros')

        else:

            form = LibroForm(
                instance=libro
            )

    # CREAR LIBRO
    else:

        if request.method == "POST":

            form = LibroForm(
                request.POST,
                request.FILES
            )

            if form.is_valid():

                form.save()

                return redirect('libros')

        else:

            form = LibroForm()

    # BUSCADOR
    busqueda = request.GET.get(
        'q',
        ''
    ).strip()

    # FILTRO POR CATEGORÍA
    categoria_id = request.GET.get(
        'categoria',
        ''
    )

    libros = Libro.objects.select_related(
        'categoria'
    ).all()

    if busqueda:

        libros = libros.filter(
            models.Q(titulo__icontains=busqueda) |
            models.Q(autor__icontains=busqueda)
        )

    if categoria_id:

        libros = libros.filter(
            categoria_id=categoria_id
        )

    categorias = Categoria.objects.all()

    # FAVORITOS
    if request.user.is_authenticated:

        favoritos_ids = Favorito.objects.filter(
            usuario=request.user
        ).values_list(
            'libro_id',
            flat=True
        )

    else:

        favoritos_ids = []

    return render(
        request,
        'biblioteca/libros.html',
        {
            'libros': libros,
            'categorias': categorias,
            'form': form,
            'editando': bool(id),
            'libro_editando': libro if id else None,
            'favoritos_ids': favoritos_ids,
            'busqueda': busqueda,
            'categoria_seleccionada': categoria_id
        }
    )

def eliminar_libro(request, id):

    libro = get_object_or_404(
        Libro,
        id=id
    )

    if request.method == "POST":

        libro.delete()

        return redirect('libros')

    return render(
        request,
        'biblioteca/eliminar_libro.html',
        {
            'libro': libro
        }
    )

def detalle_libro(request, id):

    libro = get_object_or_404(
        Libro,
        id=id
    )

    return render(
        request,
        'biblioteca/detalle_libro.html',
        {
            'libro': libro
        }
    )

def toggle_favorito(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    libro = get_object_or_404(
        Libro,
        id=id
    )

    favorito = Favorito.objects.filter(
        usuario=request.user,
        libro=libro
    ).first()

    if favorito:
        favorito.delete()
    else:
        Favorito.objects.create(
            usuario=request.user,
            libro=libro
        )

    return redirect('libros')

def favoritos(request):

    if not request.user.is_authenticated:
        return redirect('login')

    favoritos = Favorito.objects.filter(
        usuario=request.user
    ).select_related(
        'libro',
        'libro__categoria'
    )

    return render(
        request,
        'biblioteca/favoritos.html',
        {
            'favoritos': favoritos
        }
    )