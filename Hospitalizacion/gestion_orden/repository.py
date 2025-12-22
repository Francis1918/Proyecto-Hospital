from datetime import datetime
from .models import OrdenMedica

class OrdenRepository:
    def __init__(self):
        self.ordenes = {
            "P-001": [
                OrdenMedica(
                    id_orden="ORD-001",
                    id_paciente="P-001",
                    medico="Dr. Juan Pérez",
                    descripcion="Administrar antibiótico cada 8 horas",
                    fecha=datetime.now(),
                    estado="Activa"
                )
            ],
            "P-002": [
                OrdenMedica(
                    id_orden="ORD-002",
                    id_paciente="P-002",
                    medico="Dra. María López",
                    descripcion="Control de signos vitales",
                    fecha=datetime.now(),
                    estado="Activa"
                )
            ]
        }

    def obtener_por_paciente(self, id_paciente):
        return self.ordenes.get(id_paciente, [])

    def registrar(self, orden):
        self.ordenes.setdefault(orden.id_paciente, []).append(orden)

    def buscar_todas(self):
        """Retorna una lista plana de todas las órdenes para búsqueda global."""
        todas = []
        for lista in self.ordenes.values():
            todas.extend(lista)
        return todas

    def buscar_por_id(self, id_orden):
        for lista in self.ordenes.values():
            for orden in lista:
                if orden.id_orden == id_orden:
                    return orden
        return None

    def actualizar_orden(self, id_orden, nueva_descripcion):
        orden = self.buscar_por_id(id_orden)
        if orden:
            orden.descripcion = nueva_descripcion
            return True
        return False

    def anular_orden(self, id_orden):
        orden = self.buscar_por_id(id_orden)
        if orden:
            orden.estado = "Anulada"
            return True
        return False

repo_orden = OrdenRepository()
