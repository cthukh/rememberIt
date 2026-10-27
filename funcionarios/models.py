from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import FuncionarioManager
from core.validators import normalizar_rut, validar_rut


class Rol(models.Model):
    # Se guarda la clave en la db ('dir') <--> Se muestra el texto en el frontend ('Director/a')
    ROLES = {
        'dir': 'Director/a',
        'adm': 'Administrativo',
        'enf': 'Enfermero/a',
        'tec': 'Técnico',
    }

    rol_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=10, unique=True, choices=ROLES)

    def __str__(self):
        # get_nombre_display() muestra el texto ('Director/a') en lugar de la clave ('dir').
        return self.get_nombre_display()


class Funcionario(AbstractUser):
    """
    AbstractUser trae por defecto:
    password, email, first_name, last_name, is_staff, is_superuser,
    is_active, date_joined (username se elimina abajo).
    """

    # required fields
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    # fields para añadir después desde perfil
    phone_number = models.CharField(max_length=30, unique=True, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column='rol_id',
                            null=True, blank=True)

    # configuraciones extra
    USERNAME_FIELD = "rut"  # identificador (user login)
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    objects = FuncionarioManager()

    def save(self, *args, **kwargs):
        self.rut = normalizar_rut(self.rut)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - RUT: {self.rut} "

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

