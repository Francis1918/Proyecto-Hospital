try:
    from Citas_Medicas.controllers.cita_controller import CitaController
except Exception:
    from controllers.cita_controller import CitaController

class PacienteController:
    def __init__(self, cita_controller: CitaController):
        self.cita_controller = cita_controller

    def agendar_cita(self, paciente, fecha, hora, motivo):
        return self.cita_controller.agendar_cita(paciente, fecha, hora, motivo)

    def consultar_citas(self):
        return self.cita_controller.consultar_citas()

    def modificar_cita_fecha(self, id_cita, fecha):
        return self.cita_controller.modificar_fecha(id_cita, fecha)

    def modificar_cita_hora(self, id_cita, hora):
        return self.cita_controller.modificar_hora(id_cita, hora)

    def modificar_cita_fecha_hora(self, id_cita, fecha, hora):
        return self.cita_controller.modificar_fecha_hora(id_cita, fecha, hora)

    def eliminar_cita(self, id_cita):
        self.cita_controller.eliminar_cita(id_cita)
