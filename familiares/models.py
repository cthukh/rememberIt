from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Familiar(models.Model):
    rut = models.CharField(max_length=20, primary_key=True)
    primer_nombre = models.CharField(max_length=60)
    segundo_nombre = models.CharField(max_length=60, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=60)
    apellido_materno = models.CharField(max_length=60, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=255, unique=True)
    
    # Guardamos la contraseña hasheada, NUNCA en texto plano
    password = models.CharField(max_length=255) 
    
    parentesco = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.apellido_paterno} (Familiar)"

    # Método opcional para encriptar la contraseña antes de guardarla
    def save(self, *args, **kwargs):
        # Si la contraseña no está hasheada aún, la encriptamos
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)