from dateutil.relativedelta import relativedelta

def generar_fechas(recordatorio):
    pasos = {
        "DIARIA": relativedelta(days=1),
        "SEMANAL": relativedelta(weeks=1),
        "MENSUAL": relativedelta(months=1),
    }
    fechas = [recordatorio.fecha_inicio]
    if recordatorio.frecuencia == "UNA" or not recordatorio.fecha_fin:
        return fechas
    actual = recordatorio.fecha_inicio + pasos[recordatorio.frecuencia]
    while actual <= recordatorio.fecha_fin:
        fechas.append(actual)
        actual += pasos[recordatorio.frecuencia]
    return fechas