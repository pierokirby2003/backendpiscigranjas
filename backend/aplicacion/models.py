from django.db import models

# Create your models 

class Rol(models.Model):
    nombre = models.CharField(max_length=100)

class Piscigranja(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    tamano = models.DecimalField(max_digits=10, decimal_places=2)

class Estanque(models.Model):
    capacidad = models.IntegerField()
    salud = models.CharField(max_length=100)
    cantPeces = models.IntegerField()
    piscigranja = models.ForeignKey(Piscigranja, on_delete=models.CASCADE, related_name='estanque')

class MaterialNocivo(models.Model):
    nombre = models.CharField(max_length=100)
    familiaMaterial = models.ForeignKey('FamiliaMaterial', on_delete=models.PROTECT, related_name='material_nocivo')

class EstanqueMatNoc(models.Model):
    idEstanque = models.ForeignKey(Estanque, on_delete=models.CASCADE, related_name='estanque_matnoc')
    idMaterialNoc = models.ForeignKey(MaterialNocivo, on_delete=models.CASCADE, related_name='estanque_matnoc')
    fecha = models.DateField()

class FamiliaMaterial(models.Model):
    nombre = models.CharField(max_length=100)

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    idRol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='rol')

class UsuarioXPiscigranja(models.Model):
    idPiscigranja = models.ForeignKey(Piscigranja, on_delete=models.PROTECT, related_name='UsuarioXPiscigranja')
    idUsuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='UsuarioXPiscigranja')

