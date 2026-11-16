from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def siguiente(fecha, frecuencia):
    if frecuencia == "DIARIA":
        return fecha + timedelta(days=1)
    if frecuencia == "SEMANAL":
        return fecha + timedelta(weeks=1)
    if frecuencia == "MENSUAL":
        return fecha + relativedelta(months=1)
    return None  # "UNA"


def generar_fechas(recordatorio, dias_adelante=30):
    inicio = recordatorio.fecha_inicio
    if inicio is None:
        return []

    # Una sola vez: solo la fecha de inicio
    if recordatorio.frecuencia == "UNA":
        return [inicio]

    # Límite: fecha_fin, o una ventana de días si es indefinido
    if recordatorio.indefinido or recordatorio.fecha_fin is None:
        limite = max(inicio, timezone.now()) + timedelta(days=dias_adelante)
    else:
        limite = recordatorio.fecha_fin

    fechas = []
    actual = inicio
    while actual is not None and actual <= limite:
        fechas.append(actual)
        actual = siguiente(actual, recordatorio.frecuencia)
    return fechas