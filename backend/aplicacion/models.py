from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class empresas(models.Model):
    nruc=models.CharField(max_length=50)
    nombre_compañia=models.CharField(max_length=50)
    direccion_sede=models.CharField(max_length=50)
    numero_telefono=models.CharField(max_length=50)
    ciudad=models.CharField(max_length=50)
    pais=models.CharField(max_length=50)

class Piscigranja(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    tamano = models.DecimalField(max_digits=10, decimal_places=2)

class Estanque(models.Model):
    capacidad = models.IntegerField()
    salud = models.CharField(max_length=100)
    cantPeces = models.IntegerField()
    piscigranja = models.ForeignKey(Piscigranja, on_delete=models.CASCADE, related_name='estanque')

class FamiliaMaterial(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class MaterialNocivo(models.Model):
    nombre = models.CharField(max_length=100)
    familiamaterial = models.ForeignKey(FamiliaMaterial, on_delete=models.PROTECT, related_name='material_nocivo')
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return str(self.familiamaterial) + " - " + self.nombre 

class EstanqueMatNoc(models.Model):
    estanque = models.ForeignKey(Estanque, on_delete=models.CASCADE, related_name='estanque_matnoc')
    materialnoc = models.ForeignKey(MaterialNocivo, on_delete=models.CASCADE, related_name='estanque_matnoc')
    fecha = models.DateField()

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    usuario=models.CharField(max_length=100,default="0000")
    telefono=models.CharField(max_length=100,default=None)
    telefono_personal=models.CharField(max_length=100,default="0000")
    ciudad_personal=models.CharField(max_length=100,default="0000")
    pais_personal=models.CharField(max_length=100,default="0000")
    ciudad=models.CharField(max_length=100,default=None)
    pais=models.CharField(max_length=100,default=None)
    empresa=models.CharField(max_length=100,default="0000")
    nruc=models.CharField(max_length=100,default="0000")
    direccion=models.CharField(max_length=100,default="0000")
    correo = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='rol')

    def __str__(self):
        return self.nombre + " " + self.apellido
    
    @staticmethod
    def authenticate(correo, contrasena):
        try:
            user = Usuario.objects.get(correo=correo, contrasena=contrasena)
            return user
        except Usuario.DoesNotExist:
            return None

class UsuarioXPiscigranja(models.Model):
    piscigranja = models.ForeignKey(Piscigranja, on_delete=models.PROTECT, related_name='UsuarioXPiscigranja')
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='UsuarioXPiscigranja')

# Crear una fachada para simplificar operaciones comunes
class Facade:
    @staticmethod
    def get_piscigranja_by_usuario(usuario):
        try:
            return usuario.usuarioxpiscigranja.piscigranja
        except UsuarioXPiscigranja.DoesNotExist:
            return None

    @staticmethod
    def get_estanques_by_piscigranja(piscigranja):
        return piscigranja.estanque.all()

    @staticmethod
    def get_material_nocivo_by_estanque(estanque):
        return [emn.materialNoc for emn in estanque.estanque_matnoc.all()]

    @staticmethod
    def authenticate_and_get_user(correo, contrasena):
        try:
            user = Usuario.authenticate(correo, contrasena)
            return user
        except Usuario.DoesNotExist:
            return None