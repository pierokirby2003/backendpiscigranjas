from django.db import models

# Create your models 

class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

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

class MaterialNocivo(models.Model):
    nombre = models.CharField(max_length=100)
    familiaMaterial = models.ForeignKey(FamiliaMaterial, on_delete=models.PROTECT, related_name='material_nocivo')

class EstanqueMatNoc(models.Model):
    estanque = models.ForeignKey(Estanque, on_delete=models.CASCADE, related_name='estanque_matnoc')
    materialNoc = models.ForeignKey(MaterialNocivo, on_delete=models.CASCADE, related_name='estanque_matnoc')
    fecha = models.DateField()

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='rol')

    def __str__(self):
        return self.nombre + " " + self.apellido
    
class UsuarioXPiscigranja(models.Model):
    piscigranja = models.ForeignKey(Piscigranja, on_delete=models.PROTECT, related_name='UsuarioXPiscigranja')
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='UsuarioXPiscigranja')

