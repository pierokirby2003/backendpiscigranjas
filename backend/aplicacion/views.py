from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from aplicacion.models import Usuario, Rol, Piscigranja  # Asegúrate de importar los modelos adecuados
import json

@csrf_exempt
def registrar_usuario(request):
    if request.method == "POST":
        # Parsear los datos del formulario JSON
        data = json.loads(request.body)
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        correo = data.get("email")
        contrasena = data.get("contrasena")
        rol = data.get("idRol")

        # Verificar que los IDs de genero, rol y piscigranja existan en la base de datos
        try:
            rol = Rol.objects.get(pk=rol)
        except (Rol.DoesNotExist):
            return JsonResponse({"error": "ID rol no válido"}, status=400)

        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo = correo,
            contrasena=contrasena,
            rol=rol
        )
        nuevo_usuario.save()

        return JsonResponse({"mensaje": "Usuario registrado exitosamente"}, status=201)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)
    

# CORREGIR
@csrf_exempt
def iniciar_sesion(request):
    if request.method == "POST":
        # Parsear los datos del formulario JSON
        data = json.loads(request.body)
        correo = data.get("email")
        contrasena = data.get("contrasena")

        try:
            # Busca un usuario en la base de datos que coincida con el correo y la contraseña
            user = Usuario.objects.get(correo=correo, contrasena=contrasena)
            # Iniciar sesión para el usuario autenticado
            # Aquí puedes realizar alguna lógica adicional si es necesario
            # Por ejemplo, almacenar información en la sesión.
            request.session['user_id'] = user.id

            return JsonResponse({"mensaje": "Inicio de sesión exitoso"})
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Credenciales incorrectas"}, status=401)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)

    
"""
@csrf_exempt
def enviar_codigo(request):
    if request.method == "POST":
        # Generar un código de 4 dígitos aleatorio
        codigo = ''.join([str(randint(0, 9)) for _ in range(4)])

        # Envía el código al usuario (puedes implementar el envío por correo electrónico o SMS aquí)
        # Aquí asumiremos que lo enviamos en la respuesta JSON para simplificar el ejemplo.
        response_data = {"codigo": codigo}
        
        # Almacena el código temporalmente para su verificación
        request.session['codigo_verificacion'] = codigo

        return JsonResponse({"mensaje": "Código de verificación enviado con éxito", "data": response_data})

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)
        
"""

"""
@csrf_exempt
def cambiar_contraseña(request):
    if request.method == "POST":
        # Obtener el código de verificación y la nueva contraseña del formulario JSON
        data = json.loads(request.body)
        codigo_ingresado = data.get("codigo")
        nueva_contraseña = data.get("nueva_contraseña")

        # Obtener el código almacenado en la sesión
        codigo_almacenado = request.session.get('codigo_verificacion')

        if codigo_almacenado and codigo_ingresado == codigo_almacenado:
            # El código de verificación es válido, cambia la contraseña del usuario

            # Recupera al usuario cuya contraseña se va a cambiar
            # Supongamos que estás utilizando el nombre de usuario como identificación
            nombre_usuario = data.get("nombre_usuario")
            usuario = User.objects.get(username=nombre_usuario)

            # Cambia la contraseña del usuario
            usuario.set_password(nueva_contraseña)
            usuario.save()

            # Limpia el código almacenado en la sesión después de su uso
            del request.session['codigo_verificacion']

            return JsonResponse({"mensaje": "Contraseña cambiada con éxito"})
        else:
            return JsonResponse({"error": "Código de verificación incorrecto"}, status=400)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)
"""


