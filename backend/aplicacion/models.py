from django.db import models

# Create your models 

class Usuario(models.Model):
    UsuarioID = models.AutoField(primary_key=True)
    NombreUsuario = models.CharField(max_length=50, unique=False)
    Apellido = models.CharField(max_length=50, unique=False)
    Contrasena = models.CharField(max_length=50, unique=False)
    Rol = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.NombreUsuario

class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True)
    genero = models.CharField(max_length=100)

    def _str_(self):
        return self.genero

class Estanque(models.Model):
    idestanque = models.AutoField(primary_key=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.DecimalField(max_digits=10, decimal_places=2)
    estadoSalud = models.CharField(max_length=100)
    cantidadPeces = models.IntegerField()


    def _str_(self):
        return self.idestanque

class Material(models.Model):
    idmaterial = models.AutoField(primary_key=True)
    nombrematerial = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)

    def _str_(self):
        return self.nombrematerial

class MaterialesEstanque(models.Model):
    idMaterialesPiscigranja = models.AutoField(primary_key=True)
    idestanque = models.ForeignKey(Estanque, on_delete=models.CASCADE)
    idmaterial = models.ForeignKey(Material, on_delete=models.CASCADE)

    def _str_(self):
        return f'Materiales de Piscigranja #{self.idMaterialesPiscigranja}'

class PsciGranja(models.Model):
    idpscigranja = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    tamano = models.DecimalField(max_digits=10, decimal_places=2)
    idestanque = models.ForeignKey(Estanque, on_delete=models.CASCADE)

    def _str_(self):
        return self.nombre

class RegistroAlimentacion(models.Model):
    id_registro_alimentacion = models.AutoField(primary_key=True)
    fecha = models.DateField()
    tipo_alimento = models.CharField(max_length=100)
    cantidad_alimento = models.DecimalField(max_digits=10, decimal_places=2)
    idpscigranja = models.ForeignKey(PsciGranja, on_delete=models.CASCADE)

    def _str_(self):
        return f'Registro de Alimentación #{self.id_registro_alimentacion}'

class Rol(models.Model):
    id_genero = models.AutoField(primary_key=True)
    nombrerol = models.CharField(max_length=100)

    def _str_(self):
        return self.nombrerol

