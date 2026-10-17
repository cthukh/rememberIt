import re
from django.core.exceptions import ValidationError


def limpiar_rut(rut: str) -> str:
    """Quita puntos, guiones y espacios, y deja la K en mayúscula."""
    return re.sub(r"[.\-\s]", "", str(rut)).upper()


def calcular_dv(cuerpo: str) -> str:
    """Calcula el dígito verificador (módulo 11)."""
    suma = 0
    multiplicador = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
    resto = 11 - (suma % 11)
    if resto == 11:
        return "0"
    if resto == 10:
        return "K"
    return str(resto)


def normalizar_rut(rut: str) -> str:
    """Formato canónico: sin puntos, con guion (12345678-5)."""
    limpio = limpiar_rut(rut)
    if len(limpio) < 2:
        return limpio
    return f"{limpio[:-1]}-{limpio[-1]}"


def validar_rut(value: str) -> None:
    limpio = limpiar_rut(value)

    if not re.fullmatch(r"\d{7,8}[0-9K]", limpio):
        raise ValidationError(
            "El RUT debe tener 7 u 8 dígitos seguidos del dígito verificador.",
            code="rut_formato",
        )

    cuerpo, dv = limpio[:-1], limpio[-1]
    if calcular_dv(cuerpo) != dv:
        raise ValidationError(
            "El RUT ingresado no es válido (dígito verificador incorrecto).",
            code="rut_dv",
        )