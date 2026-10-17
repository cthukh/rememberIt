from django.contrib.auth.models import BaseUserManager

from .validators import normalizar_rut, validar_rut


class FuncionarioManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, rut):
        # Permite loguearse con o sin puntos y guion
        return self.get(rut=normalizar_rut(rut))

    def _create_user(self, rut, password, **extra_fields):
        if not rut:
            raise ValueError("El RUT es obligatorio.")
        validar_rut(rut)
        rut = normalizar_rut(rut)

        email = extra_fields.get("email")
        if email:
            extra_fields["email"] = self.normalize_email(email)

        user = self.model(rut=rut, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, rut, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(rut, password, **extra_fields)

    def create_superuser(self, rut, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self._create_user(rut, password, **extra_fields)