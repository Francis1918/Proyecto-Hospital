class JefeController:
    def __init__(self, agenda):
        self.agenda = agenda

    def consultar_agenda(self):
        return self.agenda.obtener_citas()

    def registrar_agenda(self):
        return "Agenda registrada correctamente"
