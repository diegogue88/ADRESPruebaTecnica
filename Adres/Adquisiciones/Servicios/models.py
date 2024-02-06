from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib import messages
from djmoney.models.fields import MoneyField, Money, Currency
from djmoney.models.validators import MaxMoneyValidator


class Registro(models.Model):
    idRegistro = models.AutoField(primary_key=True)
    Presupuesto = MoneyField(max_digits=12, decimal_places=2, default_currency='COP', validators=[MaxMoneyValidator(9999999999.99)])
    Unidad = models.CharField(max_length=150, blank=False)
    Tipo = models.CharField(max_length=150, blank=False)
    Cantidad = models.PositiveIntegerField(blank=False)
    ValorUnitario = MoneyField(max_digits=12, decimal_places=2, default_currency='COP')
    ValorTotal = MoneyField(max_digits=12, decimal_places=2, default_currency='COP', editable=False)  # Campo de dinero para ValorTotal
    FechaAdquisicion = models.DateField(null=False)
    Proveedor = models.CharField(max_length=500, blank=False)
    Documentacion = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        # Convierte Cantidad y ValorUnitario a números decimales si es necesario
        cantidad_decimal = Decimal(self.Cantidad)
        valor_unitario_decimal = self.ValorUnitario.amount

        # Calcula el ValorTotal
        valor_total_decimal = cantidad_decimal * valor_unitario_decimal

        # Asegura que el ValorTotal no sea mayor que el Presupuesto
        if valor_total_decimal > self.Presupuesto.amount:
            raise ValueError("El ValorTotal no puede ser mayor que el Presupuesto")

        self.ValorTotal = Money(valor_total_decimal, Currency('COP'))  # Asigna el ValorTotal como un objeto Money

        super().save(*args, **kwargs)

class HistorialCambios(models.Model):
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE, related_name='historialcambios_set')    
    campo_modificado = models.CharField(max_length=255)
    valor_anterior = models.CharField(max_length=255)
    nuevo_valor = models.CharField(max_length=255)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.fecha_modificacion} - {self.campo_modificado}: {self.valor_anterior} -> {self.nuevo_valor}'

