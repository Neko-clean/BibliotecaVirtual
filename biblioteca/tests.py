from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Categoria, Libro, Favorito


class BibliotecaTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(
            nombre='Ficción',
            descripcion='Novelas de ficción',
            estado=True
        )
        self.libro = Libro.objects.create(
            titulo='El Quijote',
            autor='Miguel de Cervantes',
            descripcion='Novela clásica',
            anio_publicacion=1605,
            categoria=self.categoria,
            disponible=True
        )
        self.usuario = User.objects.create_user(
            username='lector',
            email='lector@biblioteca.local',
            password='Password123'
        )

    def test_listado_libros(self):
        """El listado de libros debe devolver estado 200 y contener el libro creado."""
        response = self.client.get(reverse('libros'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El Quijote')

    def test_detalle_libro(self):
        """El detalle de un libro existente debe devolver estado 200."""
        response = self.client.get(reverse('detalle_libro', args=[self.libro.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El Quijote')

    def test_detalle_libro_inexistente(self):
        """El detalle de un libro inexistente debe devolver 404."""
        response = self.client.get(reverse('detalle_libro', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_crear_libro(self):
        """Crear un libro mediante POST debe agregar un libro al catálogo."""
        response = self.client.post(reverse('libros'), {
            'titulo': 'Cien años de soledad',
            'autor': 'Gabriel García Márquez',
            'descripcion': 'Realismo mágico',
            'anio_publicacion': 1967,
            'categoria': self.categoria.id,
            'disponible': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Libro.objects.filter(titulo='Cien años de soledad').exists())

    def test_editar_libro(self):
        """Editar un libro existente debe actualizar sus datos."""
        response = self.client.post(reverse('editar_libro', args=[self.libro.id]), {
            'titulo': 'El Quijote (editado)',
            'autor': 'Miguel de Cervantes',
            'descripcion': 'Novela clásica editada',
            'anio_publicacion': 1605,
            'categoria': self.categoria.id,
            'disponible': True
        })
        self.assertEqual(response.status_code, 302)
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.titulo, 'El Quijote (editado)')

    def test_eliminar_libro(self):
        """Eliminar un libro debe borrarlo del catálogo."""
        response = self.client.post(reverse('eliminar_libro', args=[self.libro.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Libro.objects.filter(id=self.libro.id).exists())

    def test_listado_categorias(self):
        """El listado de categorías debe devolver estado 200."""
        response = self.client.get(reverse('categorias'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ficción')

    def test_crear_categoria(self):
        """Crear una categoría mediante POST debe agregarla."""
        response = self.client.post(reverse('categorias'), {
            'nombre': 'Historia',
            'descripcion': 'Libros de historia',
            'estado': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Categoria.objects.filter(nombre='Historia').exists())

    def test_editar_categoria(self):
        """Editar una categoría existente debe actualizar sus datos."""
        response = self.client.post(reverse('editar_categoria', args=[self.categoria.id]), {
            'nombre': 'Ficción editada',
            'descripcion': 'Novelas de ficción editada',
            'estado': True
        })
        self.assertEqual(response.status_code, 302)
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nombre, 'Ficción editada')

    def test_favoritos_requiere_autenticacion(self):
        """Acceso a favoritos sin autenticación debe redirigir a login."""
        response = self.client.get(reverse('favoritos'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_favoritos_autenticado(self):
        """Acceso a favoritos autenticado debe devolver estado 200."""
        self.client.login(username='lector', password='Password123')
        Favorito.objects.create(usuario=self.usuario, libro=self.libro)
        response = self.client.get(reverse('favoritos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El Quijote')

    def test_toggle_favorito_requiere_autenticacion(self):
        """toggle_favorito sin autenticación debe redirigir a login."""
        response = self.client.get(reverse('toggle_favorito', args=[self.libro.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_toggle_favorito_agrega_y_quita(self):
        """toggle_favorito autenticado debe agregar y quitar el libro de favoritos."""
        self.client.login(username='lector', password='Password123')

        # Agregar a favoritos
        response = self.client.get(reverse('toggle_favorito', args=[self.libro.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favorito.objects.filter(usuario=self.usuario, libro=self.libro).exists())

        # Quitar de favoritos
        response = self.client.get(reverse('toggle_favorito', args=[self.libro.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Favorito.objects.filter(usuario=self.usuario, libro=self.libro).exists())

    def test_busqueda_libros(self):
        """Buscar libros por título debe filtrar los resultados."""
        response = self.client.get(reverse('libros') + '?q=Quijote')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El Quijote')

        response = self.client.get(reverse('libros') + '?q=Inexistente')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'El Quijote')
