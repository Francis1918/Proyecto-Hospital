from .models import OrdenMedica

class OrdenRepository:
    def __init__(self):
        self.ordenes = {}

    def registrar(self, orden: OrdenMedica):
        self.ordenes.setdefault(orden.id_paciente, []).append(orden)

    def obtener_por_paciente(self, id_paciente: str):
        return self.ordenes.get(id_paciente, [])

orden_repo = OrdenRepository()
