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
    path('register/', views.registrar_usuario),
    path('enviar_codigo/', views.enviar_codigo),
    #path('cambiar_contraseña/', views.cambiar_contraseña),
    path('verificar_codigo/', views.verificar_codigo),
    path('obtener_conteo_materiales/', views.obtener_conteo_materiales),
    path('cambiar_contrasena/', views.cambiar_contrasena),
    #path('test/', views.test)
]
