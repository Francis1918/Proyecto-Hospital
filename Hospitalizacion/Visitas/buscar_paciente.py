from .datos_simulados import pacientes

def buscar_paciente(cedula):
    """
    Busca un paciente por su cédula en los datos simulados.
    :param cedula: str - Cédula del paciente a buscar.
    :return: dict - Información del paciente si se encuentra, None si no existe.
    """
    for paciente in pacientes:
        if paciente["cedula"] == cedula:
            return paciente
    return None

# Prueba de la función
if __name__ == "__main__":
    cedula = input("Ingrese la cédula del paciente: ")
    resultado = buscar_paciente(cedula)
    if resultado:
        print(f"Paciente encontrado: {resultado}")
    else:
        print("Paciente no registrado.")