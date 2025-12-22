try:
    from Citas_Medicas.controllers.cita_controller import CitaController
except Exception:
    from controllers.cita_controller import CitaController

class RecepcionistaController:
    def __init__(self, cita_controller: CitaController):
        self.cita_controller = cita_controller

    def agendar_cita(self, paciente, fecha, hora, motivo):
        return self.cita_controller.agendar_cita(paciente, fecha, hora, motivo)

    def consultar_citas(self):
        return self.cita_controller.consultar_citas()

    def eliminar_cita(self, id_cita):
        self.cita_controller.eliminar_cita(id_cita)
