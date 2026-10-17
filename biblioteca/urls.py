from django.urls import path
from . import views

urlpatterns = [

    path('categorias/',views.categorias,name='categorias'),
    path('categorias/editar/<int:id>/',views.editar_categoria,name='editar_categoria'),
    path('libros/',views.libros,name='libros'),
    path('libros/editar/<int:id>/',views.libros,name='editar_libro'),
    path('libros/eliminar/<int:id>/',views.eliminar_libro,name='eliminar_libro'),
    path('libros/<int:id>/', views.detalle_libro, name='detalle_libro'),
    path('libros/favorito/<int:id>/',views.toggle_favorito,name='toggle_favorito'),
    path('favoritos/',views.favoritos,name='favoritos'),

]