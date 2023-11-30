# Importa los módulos necesarios
import json
from django.test import TestCase, Client
from django.urls import reverse
from aplicacion.models import Usuario, Rol

class RegistrarUsuarioTest(TestCase):

    def setUp(self):
        # Crea un rol de ejemplo para usar en las pruebas
        self.rol = Rol.objects.create(nombre="EjemploRol")

        # Datos de usuario de ejemplo
        self.datos_usuario = {
            "nombre": "EjemploNombre",
            "apellido": "EjemploApellido",
            "email": "ejemplo@correo.com",
            "password": "contrasena123",
            "telefono": "123456789",
            "ciudad": "EjemploCiudad",
            "pais": "EjemploPais",
            "empresa": "EjemploEmpresa",
            "nruc": "12345678901",
            "direccion": "EjemploDireccion",
            "idRol": self.rol.id
        }

    def test_registrar_usuario_exitoso(self):
        # Hacer una solicitud POST al endpoint de registro
        response = self.client.post(reverse('registrar_usuario'), json.dumps(self.datos_usuario), content_type="application/json")

        # Verificar que la respuesta sea 201 Created
        self.assertEqual(response.status_code, 201)

        # Verificar que el usuario se ha creado en la base de datos
        usuario_creado = Usuario.objects.get(correo=self.datos_usuario["email"])
        self.assertIsNotNone(usuario_creado)

        # Verificar el mensaje de la respuesta
        self.assertEqual(response.json()["mensaje"], "Usuario registrado exitosamente")

    def test_registrar_usuario_con_rol_invalido(self):
        # Modificar los datos de usuario para tener un ID de rol no válido
        datos_usuario_rol_invalido = self.datos_usuario.copy()
        datos_usuario_rol_invalido["idRol"] = 999  # Un ID de rol que no existe

        # Hacer una solicitud POST al endpoint de registro
        response = self.client.post(reverse('registrar_usuario'), json.dumps(datos_usuario_rol_invalido), content_type="application/json")

        # Verificar que la respuesta sea 400 Bad Request (ID de rol no válido)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "ID rol no válido")

    # Puedes agregar más pruebas según tus necesidades

# Asegúrate de reemplazar 'nombre_de_tu_url_registrar_usuario' con el nombre real de tu URL de registro de usuario
