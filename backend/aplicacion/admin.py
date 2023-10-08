from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Genero)
admin.site.register(Estanque)
admin.site.register(Material)
admin.site.register(MaterialesEstanque)
admin.site.register(PsciGranja)
admin.site.register(RegistroAlimentacion)
admin.site.register(Rol)

