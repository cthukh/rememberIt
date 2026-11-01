from django.db import models
from residentes.models import Residente
import uuid


class Recordatorio(models.Model):

    FRECUENCIA_CHOICES = [
        ("UNA", "Una vez"),
        ("DIARIA", "Diaria"),
        ("SEMANAL", "Semanal"),
        ("MENSUAL", "Mensual"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    frecuencia = models.CharField(max_length=10, choices=FRECUENCIA_CHOICES, default="UNA")
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)

    residente = models.ForeignKey(
        Residente, on_delete=models.PROTECT,
        null=True, blank=True, db_column='residente_rut',related_name="recordatorios"
    )

    def __str__(self):
        return self.nombre

    @property
    def cumplido(self):
        return not self.fechas.filter(cumplido=False).exists()


class FechaRecordatorio(models.Model):

    ESTADO_CHOICES = [
        (False, "Pendiente"),
        (True, "Cumplido"),
    ]

    recordatorio = models.ForeignKey(
        Recordatorio, on_delete=models.CASCADE, related_name="fechas"
    )
    fecha_hora = models.DateTimeField()
    cumplido = models.BooleanField(default=False, choices=ESTADO_CHOICES)

    class Meta:
        ordering = ["fecha_hora"]
        unique_together = ("recordatorio", "fecha_hora")

    def __str__(self):
        return f"{self.recordatorio.nombre} - {self.fecha_hora:%d/%m/%Y %H:%M}"