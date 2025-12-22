class Usuario:
    def __init__(self, id_usuario: int, nombre: str, rol: str):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.rol = rol  # Paciente | Recepcionista | Jefe
