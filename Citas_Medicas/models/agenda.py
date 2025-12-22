class Agenda:
    def __init__(self):
        self.citas = []

    def agregar_cita(self, cita):
        self.citas.append(cita)

    def eliminar_cita(self, id_cita):
        self.citas = [c for c in self.citas if c.id_cita != id_cita]

    def obtener_citas(self):
        return self.citas

    def buscar_cita(self, id_cita):
        for cita in self.citas:
            if cita.id_cita == id_cita:
                return cita
        return None
