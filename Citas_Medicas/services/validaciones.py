import re

def validar_fecha(fecha: str) -> bool:
    # Formato YYYY-MM-DD
    patron = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(patron, fecha) is not None


def validar_hora(hora: str) -> bool:
    # Formato HH:MM
    patron = r"^\d{2}:\d{2}$"
    return re.match(patron, hora) is not None


def existe_conflicto(agenda, fecha, hora) -> bool:
    for cita in agenda.obtener_citas():
        if cita.fecha == fecha and cita.hora == hora:
            return True
    return False


def validar_cedula(cedula: str) -> bool:
    """
    Valida un formato simple de cédula: solo dígitos, entre 6 y 10 caracteres.
    Ajustar la expresión regular según reglas locales si es necesario.
    """
    patron = r"^\d{6,10}$"
    return re.match(patron, cedula) is not None
