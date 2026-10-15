from django.db import models

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


class Funcionario(models.Model):
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
    def __str__(self):
        return f"{self.primer_nombre} {self.apellido_paterno} - RUT: {self.rut}"

    @property
    def full_name(self):
        """Retorna el nombre completo considerando opcionales."""
        segundo = f" {self.segundo_nombre}" if self.segundo_nombre else ""
        materno = f" {self.apellido_materno}" if self.apellido_materno else ""
        return f"{self.primer_nombre}{segundo} {self.apellido_paterno}{materno}"