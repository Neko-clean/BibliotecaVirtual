from django import forms
from .models import Categoria, Libro


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria

        fields = [
            'nombre',
            'descripcion',
            'estado'
        ]

        widgets = {

            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción (opcional)'
            }),

            'estado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class LibroForm(forms.ModelForm):

    class Meta:
        model = Libro

        fields = [
            'titulo',
            'autor',
            'descripcion',
            'portada',
            'anio_publicacion',
            'categoria',
            'disponible'
        ]

        widgets = {

            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del libro'
            }),

            'autor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del autor'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del libro'
            }),

            'portada': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),

            'anio_publicacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. 2026'
            }),

            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),

            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }