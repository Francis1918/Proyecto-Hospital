class Cita:
    def __init__(self, id_cita: int, paciente: str, fecha: str, hora: str, motivo: str):
        self.id_cita = id_cita
        self.paciente = paciente
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo

    def actualizar_fecha(self, nueva_fecha: str):
        self.fecha = nueva_fecha

    def actualizar_hora(self, nueva_hora: str):
        self.hora = nueva_hora

    def actualizar_fecha_hora(self, nueva_fecha: str, nueva_hora: str):
        self.fecha = nueva_fecha
        self.hora = nueva_hora
