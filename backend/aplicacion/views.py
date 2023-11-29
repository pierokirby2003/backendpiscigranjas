from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from aplicacion.models import Usuario, Rol, MaterialNocivo,EstanqueMatNoc,Piscigranja,empresas  # Asegúrate de importar los modelos adecuados
import json
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.db import connection

@csrf_exempt
def registrar_usuario(request):
    if request.method == "POST":
        # Parsear los datos del formulario JSON
        data = json.loads(request.body)
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        correo = data.get("email")
        contrasena = data.get("password")
        #rol = data.get("idRol")
        rol = "2"
        telefono=data.get("telefono")
        ciudad=data.get("ciudad")
        pais=data.get("pais")
        empresa=data.get("empresa")
        nruc=data.get("nruc")
        direccion=data.get("direccion")
        # Verificar rol existan en la base de datos
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
            rol=rol,
            telefono=telefono,
            ciudad=ciudad,
            pais=pais,
            empresa=empresa,
            nruc=nruc,
            direccion=direccion
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
        contrasena = data.get("password")
        try:
            # Busca un usuario en la base de datos que coincida con el correo y la contraseña
            user = Usuario.objects.get(correo=correo, contrasena=contrasena)
            print(user)
            # Iniciar sesión para el usuario autenticado
            if user:
                dictOK={
                    "error":"Inicio de sesión exitoso"
                }
                return JsonResponse(dictOK)
            
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Credenciales incorrectas"}, status=401)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)


codigo_almacenado = ""
correo_temp = ""

@csrf_exempt
def enviar_codigo(request):
    global codigo_almacenado
    global correo_temp
    if request.method == "POST":
        # Generar un código de 4 dígitos aleatorio
        data = json.loads(request.body)
        correo = data.get("email")
        correo_temp = correo
        print(data)
        codigo = ''.join([str(randint(0, 9)) for _ in range(4)])
        # Envía el código al usuario (puedes implementar el envío por correo electrónico o SMS aquí)
        # Aquí asumiremos que lo enviamos en la respuesta JSON para simplificar el ejemplo.
        response_data = {"codigo": codigo}
        
        # Almacena el código temporalmente para su verificación
        request.session['codigo_verificacion'] = codigo
        print(request.session['codigo_verificacion'])
        codigo_almacenado = request.session['codigo_verificacion']
        print("este es el codigo almacenado:",codigo_almacenado)
        #session_id = request.session.session_key
        #print("session_id:", session_id)
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [correo]
        send_mail("Envio de codigo", codigo, email_from, recipient_list)
        #test(request)
        return JsonResponse({"mensaje": "Código de verificación enviado con éxito", "data": response_data})

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)
        
"""@csrf_exempt
def test(request):
        print("Este es del test: ", request.session['codigo_verificacion'])
        return request.session['codigo_verificacion']"""


@csrf_exempt
def verificar_codigo(request):
    if request.method == "POST":
        # Obtener el código de verificación del formulario JSON
        data = json.loads(request.body)
        codigo_ingresado = data.get("resultado")
        print(codigo_ingresado)
        print(codigo_almacenado)
        
        # Si el código almacenado coincide con el código ingresado
        if codigo_almacenado == codigo_ingresado:
            dictOK={
                    "error":""
                }
            return JsonResponse(dictOK)
        else:
            return JsonResponse({"error": "Código de verificación incorrecto"}, status=400)
    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)

    

"""
@csrf_exempt
def cambiar_contraseña(request):
    if request.method == "POST":
        # Obtener el código de verificación y la nueva contraseña del formulario JSON
        data = json.loads(request.body)
        codigo_ingresado = data.get("codigo")
        nueva_contraseña = data.get("nueva_contraseña")

        # Obtener el código almacenado en la sesión
        #codigo_almacenado = request.session.get('codigo_verificacion')

        if codigo_almacenado and codigo_ingresado == codigo_almacenado:
            # El código de verificación es válido, cambia la contraseña del usuario

            # Recupera al usuario cuya contraseña se va a cambiar
            # Supongamos que estás utilizando el nombre de usuario como identificación
            correo = data.get("correo")
            usuario = Usuario.objects.get(username=correo)

            # Cambia la contraseña del usuario
            usuario["contrasena"] = nueva_contraseña
            #usuario.set_password(nueva_contraseña)
            usuario.save()

            # Limpia el código almacenado en la sesión después de su uso
            del request.session['codigo_verificacion']

            return JsonResponse({"mensaje": "Contraseña cambiada con éxito"})
        else:
            return JsonResponse({"error": "Código de verificación incorrecto"}, status=400)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)
    """


@csrf_exempt
def obtener_conteo_materiales(request):
    # Ejecuta una consulta SQL personalizada
    with connection.cursor() as cursor:
        cursor.execute("select B.nombre as nombre, count(*) as cantidad from aplicacion_EstanqueMatNoc as A inner join aplicacion_MaterialNocivo as B on a.materialnoc_id = b.id group by nombre")
        results = cursor.fetchall()

    # Procesa los resultados y crea una respuesta
    response_data = [{"nombre": nombre, "cantidad": cantidad} for nombre, cantidad in results]
    print(response_data)
    return JsonResponse(response_data, safe=False)


"""@csrf_exempt
def obtener_columnas(request):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM aplicacion_materialnocivo LIMIT 0")
        columns = [col_desc[0] for col_desc in cursor.description]
        print(columns)
    return columns"""


# Esto es parte de HU14: te da TODA la lista de materiales
@csrf_exempt
def obtener_lista_materiales(request):
    # Ejecuta una consulta SQL personalizada con parámetros
    with connection.cursor() as cursor:
        cursor.execute("SELECT A.nombre as nombre, A.descripcion FROM aplicacion_materialnocivo as A")
        results = cursor.fetchall()

    # Procesa los resultados y crea una respuesta
    response_data = [{"Nombre de material": nombre, "descripcion": descripcion} for nombre, descripcion in results]
    print(response_data)
    return JsonResponse(response_data, safe=False)




# Esto es parte de HU14: te da la lista de materiales por nombre de material ingresado
@csrf_exempt
def obtener_lista_materialesxnombre(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nombre = data.get("nombre")

        # Ejecuta una consulta SQL personalizada con parámetros
        with connection.cursor() as cursor:
            cursor.execute("SELECT A.nombre as nombre, A.descripcion FROM aplicacion_materialnocivo as A WHERE A.nombre = %s", [nombre])
            results = cursor.fetchall()

        # Procesa los resultados y crea una respuesta
        response_data = [{"Nombre de material": nombre, "descripcion": descripcion} for nombre, descripcion in results]
        print(response_data)
        return JsonResponse(response_data, safe=False)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)


# Esto es parte de HU14: te da la lista de materiales por categoria ingresada
@csrf_exempt
def obtener_lista_materialesxcategoria(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nombre_familia = data.get("nombre_familia")

        # Ejecuta una consulta SQL personalizada con parámetros
        with connection.cursor() as cursor:
            cursor.execute("SELECT A.nombre as nombre, A.descripcion FROM aplicacion_materialnocivo as A INNER JOIN aplicacion_familiamaterial as B ON a.familiaMaterial_id = B.id WHERE B.nombre = %s", [nombre_familia])
            results = cursor.fetchall()

        # Procesa los resultados y crea una respuesta
        response_data = [{"Nombre de material": nombre, "descripcion": descripcion} for nombre, descripcion in results]
        print(response_data)
        return JsonResponse(response_data, safe=False)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)

    

@csrf_exempt
def cambiar_contrasena(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        #usuario_id = data.get("correo")
        correo = correo_temp
        nueva_contrasena = data.get("password")
        print(nueva_contrasena)
        try:
            #usuario = Usuario.objects.get(pk=usuario_id)
            usuario = Usuario.objects.get(correo = correo)
            usuario.contrasena = nueva_contrasena
            usuario.save()
            return JsonResponse({"mensaje": "Contraseña cambiada con éxito"})
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)
    
@csrf_exempt
def configurar_perfil(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nombre = data.get("nombre")
        correo= data.get("email")
        apellido=data.get("apellido")
        telefono=data.get("telefono")
        ciudad=data.get("ciudad")
        pais=data.get("pais")
        try:
            #usuario = Usuario.objects.get(pk=usuario_id)
            usuario = Usuario.objects.get(correo = correo)
            usuario.nombre=nombre
            usuario.apellido=apellido
            usuario.telefono_personal=telefono
            usuario.ciudad_personal=ciudad
            usuario.pais_personal=pais
            usuario.save()
            return JsonResponse({"error": ""})
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)
    
@csrf_exempt
def validar_ruc(request):
    if request.method == "POST":
        # Parsear los datos del formulario JSON
        data = json.loads(request.body)
        ruc = data.get("ruc")
        try:
            # Busca un usuario en la base de datos que coincida con el correo y la contraseña
            empresa = empresas.objects.get(nruc=ruc)
            print(empresa)
            # Iniciar sesión para el usuario autenticado
            if empresa:
                dictOK={
                    "ruc":empresa.nruc,
                    "telefono":empresa.numero_telefono,
                    "sede":empresa.direccion_sede,
                    "compañia":empresa.nombre_compañia,
                    "ciudad":empresa.ciudad,
                    "pais":empresa.pais
                }
                return JsonResponse(dictOK)
            
        except empresas.DoesNotExist:
            return JsonResponse({"error": "ruc no existe incorrectas"}, status=401)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)
@csrf_exempt
def obtener_usuario(request):
    if request.method == "POST":
        # Parsear los datos del formulario JSON
        data = json.loads(request.body)
        email = data.get("email")
        try:
            # Busca un usuario en la base de datos que coincida con el correo y la contraseña
            usuario = Usuario.objects.filter(correo=email).first()
            print(usuario)
            # Iniciar sesión para el usuario autenticado
            if usuario:
                dictOK={
                    "nombre":usuario.nombre,
                    "apellido":usuario.apellido,
                    "telefono_personal":usuario.telefono_personal,
                    "correo":usuario.correo,
                    "ciudad_personal":usuario.ciudad_personal,
                    "pais_personal":usuario.pais_personal,
                    "compañia":usuario.empresa,
                    "nruc":usuario.nruc,
                    "sede":usuario.direccion,
                    "telefono_empresa":usuario.telefono,
                    "ciudad":usuario.ciudad,
                    "pais":usuario.pais

                }
                return JsonResponse(dictOK)
            
        except empresas.DoesNotExist:
            return JsonResponse({"error": "ruc no existe incorrectas"}, status=401)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405) 


correo_soporte = "piscigranjadanitahs@gmail.com"
# HU08: Comunicacion con soporte
@csrf_exempt
def enviar_correo_soporte(request):
    global correo_soporte
    if request.method == "POST":
        # Generar un código de 4 dígitos aleatorio
        data = json.loads(request.body)
        asunto = data.get("asunto")
        mensaje = "Se confirma el envío de tu ticket\n Este es el mensaje:" + data.get("mensaje")
        print(data)
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [correo_soporte]
        send_mail(asunto, mensaje, email_from, recipient_list,)
        #test(request)
        return JsonResponse({"mensaje": "Correo enviado con éxito"})

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)
    



# HU10: Comunicacion con entidad reguladora
@csrf_exempt
def enviar_correo_entidad(request):
    if request.method == "POST":
        # Generar un código de 4 dígitos aleatorio
        data = json.loads(request.body)
        correo_entidad = data.get("email")
        asunto = data.get("asunto")
        mensaje = data.get("mensaje")
        print(data)
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [correo_entidad]
        send_mail(asunto, mensaje, email_from, recipient_list)
        #test(request)
        return JsonResponse({"mensaje": "Correo enviado con éxito"})

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)

from django.http import JsonResponse

@csrf_exempt
def estanques_por_usuario(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            usuario_id = data.get("email")
            usuario_id = "renzosaucedos@gmail.com"
            usuario = Usuario.objects.get(correo=usuario_id)
            piscigranja = usuario.piscigranja_set.first()  # Suponiendo que un usuario solo tiene una piscigranja
            estanques = piscigranja.estanque.all()
            estanques_data = [
                {
                    'id': estanque.id,
                    'capacidad': estanque.capacidad,
                    'salud': estanque.salud,
                    'cantPeces': estanque.cantPeces,
                    'piscigranja': estanque.piscigranja_id
                }
                for estanque in estanques
            ]
            return JsonResponse(estanques_data, safe=False)
    except Usuario.DoesNotExist:
        return JsonResponse([], safe=False)

