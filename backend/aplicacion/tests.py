from django.test import TestCase
from django.test import Client
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_registrar_usuario(self):
        data = {
            "nombre": "Nombre",
            "apellido": "Apellido",
            "email": "correo@example.com",
            "password": "contraseña",
            "idRol": "2"
        }
        response = self.client.post('/ruta_de_tu_vista/registrar_usuario/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Verificar que el usuario se haya registrado exitosamente

    def test_iniciar_sesion(self):
        data = {
            "email": "correo@example.com",
            "password": "contraseña"
        }
        response = self.client.post('/ruta_de_tu_vista/iniciar_sesion/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Verificar que el inicio de sesión sea exitoso

    # Continuar con pruebas similares para otras funciones...

    def test_obtener_conteo_materiales(self):
        response = self.client.get('/ruta_de_tu_vista/obtener_conteo_materiales/')
        self.assertEqual(response.status_code, 200)  # Verificar que se obtenga el conteo de materiales correctamente
        self.assertTrue(len(response.json()) > 0)  # Verificar que se reciba al menos un resultado
