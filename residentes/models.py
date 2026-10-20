from django.db import models
from funcionarios.models import Funcionario
from familiares.models import Familiar

class Residente(models.Model):
    Estados=[('activo', 'Activo'),('inactivo', 'Inactivo')]
    Sangre=[('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-')]

    rut = models.CharField(max_length=15, primary_key=True, unique=True)
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=Estados, default='inactivo')
    fecha_nacimiento = models.DateField()
    tipo_sangre = models.CharField(max_length=3, choices=Sangre, blank=True, null=True)
    edad = models.PositiveIntegerField()
    alergias = models.TextField(max_length=255, blank=True, null=True)
    telefono_emergencias = models.CharField(max_length=15, blank=True, null=True)
    antecedentes_medicos = models.TextField(max_length=255, blank=True, null=True)
    
    # Relación con el funcionario que lo registró/supervisa
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, db_column='funcionario_rut')
    
    # Relación con el familiar a cargo (puede ser nulo si aún no está asignado)
    familiar = models.ForeignKey(Familiar, on_delete=models.SET_NULL, null=True, blank=True, db_column='familiar_rut')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.apellido_paterno} ({self.rut})"