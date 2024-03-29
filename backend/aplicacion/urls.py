"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# Se pone "." porque este archivo y views están en el mismo nivel de directorio
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('login/', views.iniciar_sesion),
    path('register/', views.registrar_usuario, name = 'registrar_usuario'),
    path('enviar_codigo/', views.enviar_codigo),
    #path('cambiar_contraseña/', views.cambiar_contraseña),
    path('verificar_codigo/', views.verificar_codigo),
    path('obtener_conteo_materiales/', views.obtener_conteo_materiales),
    path('obtener_conteo_materialesxmes/', views.obtener_conteo_materialesxmes),
    path('obtener_lista_materiales/', views.obtener_lista_materiales),
    path('obtener_lista_materialesxcategoria/', views.obtener_lista_materialesxcategoria),
    path('obtener_lista_materialesxnombre/', views.obtener_lista_materialesxnombre),
    path('enviar_correo_entidad/', views.enviar_correo_entidad),
    path('enviar_correo_soporte/', views.enviar_correo_soporte),
    path('solicitar_limpieza/', views.solicitar_limpieza),
    path('cambiar_contrasena/', views.cambiar_contrasena),
    path('configurar_perfil/', views.configurar_perfil),
    path('validarruc/',views.validar_ruc),
    path('obtener_usuario/',views.obtener_usuario),
    path('obtener_estanques/',views.estanques_por_usuario)
    #path('obtener_columnas/', views.obtener_columnas)
    #path('test/', views.test)
]
