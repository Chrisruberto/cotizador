from django.db import models

class Dolar(models.Model):
    nombre = models.CharField(max_length=100)
    compra = models.DecimalField(max_digits=10, decimal_places=2)
    venta = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_actualizacion = models.DateTimeField()

    def __str__(self):
        return self.nombre