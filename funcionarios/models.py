from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# 1. Creamos un Manager personalizado para manejar el RUT como identificador principal
# Para crear superusuarios desde consola
class FuncionarioManager(BaseUserManager):
    def create_user(self, rut, password=None, **extra_fields):
        if not rut:
            raise ValueError("El RUT es obligatorio")
        user = self.model(rut=rut, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rut, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(rut, password, **extra_fields)

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
        # get_nombre_display() es un método mágico que Django crea automáticamente 
        # para mostrar el texto de la derecha ('Director/a') en lugar de la clave ('dir').
        return self.get_nombre_display()


class Funcionario(AbstractUser):
    # Desactivamos el username por defecto de Django para usar el RUT
    username = None  
    rut              = models.CharField(max_length=20, primary_key=True)
    
    primer_nombre    = models.CharField(max_length=60)
    segundo_nombre   = models.CharField(max_length=60, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=60)
    apellido_materno = models.CharField(max_length=60, blank=True, null=True)
    
    direccion        = models.TextField()
    telefono         = models.CharField(max_length=20, unique=True)
    correo           = models.EmailField(max_length=255, unique=True)
    
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column='rol_id', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # 2. Conectamos el Manager personalizado al modelo
    objects = FuncionarioManager()

    # Configuramos el sistema de login para que use el RUT
    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['primer_nombre', 'apellido_paterno', 'email']

    def __str__(self):
        return f"{self.primer_nombre} {self.apellido_paterno} - RUT: {self.rut}"

    @property
    def full_name(self):
        """Retorna el nombre completo considerando opcionales."""
        segundo = f" {self.segundo_nombre}" if self.segundo_nombre else ""
        materno = f" {self.apellido_materno}" if self.apellido_materno else ""
        return f"{self.primer_nombre}{segundo} {self.apellido_paterno}{materno}"