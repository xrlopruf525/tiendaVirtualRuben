from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=100, blank = False, null=True )
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100, blank = False, null=True )
    modelo = models.CharField(max_length=100, blank = False, null=True )
    unidades = models.IntegerField( blank = False)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    vip = models.BooleanField(default= False)
    marca = models.ForeignKey(Marca,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre} ({self.modelo}), {self.precio}"

class Usuario(AbstractUser):
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vip = models.BooleanField(default= False)
    def __str__(self):  
        return f'Cliente Nº{self.pk}'

class Compra(models.Model):
    class Iva(models.TextChoices):
        Iva_4 = '4%'
        Iva_10 = '10%'
        Iva_21 = '21%'
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='compras')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='compras')
    fecha =  models.DateField(auto_now_add=True)
    unidades = models.IntegerField( blank = False)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.CharField(max_length= 3, choices=Iva.choices, default='')
    def __str__(self):
        return f'{self.usuario} {self.fecha}'

class Promocion(models.Model): 
    nombre = models.CharField(max_length=100, blank = False, null=True )
    codigo = models.IntegerField()
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    def __str__(self):
        return self.nombre


