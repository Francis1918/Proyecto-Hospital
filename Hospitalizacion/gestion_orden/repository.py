class OrdenRepository:
    def __init__(self):
        self.ordenes = {}

    def registrar_orden(self, orden: OrdenMedica):
        self.ordenes.setdefault(orden.id_paciente, []).append(orden)

    def obtener_ordenes(self, id_paciente: str):
        return self.ordenes.get(id_paciente, [])
