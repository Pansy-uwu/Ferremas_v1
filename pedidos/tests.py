from rest_framework.test import APITestCase
from .models import Producto

class ProductoAPITestCase(APITestCase):
    def setUp(self):
        Producto.objects.create(
            codigo="FER-12345",
            nombre="Taladro Percutor Bosch",
            descripcion="Taladro de alta calidad",
            precio=89090.99,
            marca="Bosch",
            stock=10,
            disponible=True
        )

    def test_lista_productos(self):
        response = self.client.get('/api/productos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
