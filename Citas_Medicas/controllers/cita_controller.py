from typing import Optional

try:
    from Citas_Medicas.models.cita import Cita
    from Citas_Medicas.services import validaciones
except Exception:
    from models.cita import Cita
    from services import validaciones


class CitaController:
    """Controlador que implementa las reglas de negocio para gestionar citas.

    - Valida campos obligatorios
    - Valida formatos de fecha y hora
    - Evita conflictos (misma fecha y hora)
    - Registra `Cita` en la `Agenda`
    """

    def __init__(self, agenda):
        self.agenda = agenda

    def crear_cita(self, paciente: str, fecha: str, hora: str, motivo: str) -> Cita:
        return self.agendar_cita(paciente, fecha, hora, motivo)

    def agendar_cita(self, paciente: str, fecha: str, hora: str, motivo: str) -> Cita:
        # Validaciones básicas
        if not paciente or not fecha or not hora:
            raise ValueError("Todos los campos obligatorios deben completarse")

        if not validaciones.validar_fecha(fecha):
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")

        if not validaciones.validar_hora(hora):
            raise ValueError("Formato de hora inválido. Use HH:MM")

        # Comprueba conflictos en la agenda
        if validaciones.existe_conflicto(self.agenda, fecha, hora):
            raise ValueError("Ya existe una cita en esa fecha y hora")

        # Generar id incremental
        try:
            next_id = max((c.id_cita for c in self.agenda.obtener_citas()), default=0) + 1
        except Exception:
            next_id = 1

        nueva_cita = Cita(next_id, paciente, fecha, hora, motivo)
        # Registrar en el modelo
        self.agenda.agregar_cita(nueva_cita)
        return nueva_cita

    def eliminar_cita(self, id_cita: int) -> None:
        self.agenda.eliminar_cita(id_cita)

    def listar_citas(self):
        return self.agenda.obtener_citas()

    def consultar_citas(self):
        return self.listar_citas()

    def modificar_fecha(self, id_cita: int, nueva_fecha: str) -> bool:
        if not validaciones.validar_fecha(nueva_fecha):
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")

        for cita in self.agenda.obtener_citas():
            if cita.id_cita == id_cita:
                # comprobar conflicto con misma hora
                if validaciones.existe_conflicto(self.agenda, nueva_fecha, cita.hora):
                    raise ValueError("Ya existe una cita en esa fecha y hora")
                cita.actualizar_fecha(nueva_fecha)
                return True
        raise ValueError("La cita no existe")

    def modificar_hora(self, id_cita: int, nueva_hora: str) -> bool:
        if not validaciones.validar_hora(nueva_hora):
            raise ValueError("Formato de hora inválido. Use HH:MM")

        for cita in self.agenda.obtener_citas():
            if cita.id_cita == id_cita:
                if validaciones.existe_conflicto(self.agenda, cita.fecha, nueva_hora):
                    raise ValueError("Ya existe una cita en esa fecha y hora")
                cita.actualizar_hora(nueva_hora)
                return True
        raise ValueError("La cita no existe")

    def modificar_fecha_hora(self, id_cita: int, nueva_fecha: str, nueva_hora: str) -> bool:
        if not validaciones.validar_fecha(nueva_fecha) or not validaciones.validar_hora(nueva_hora):
            raise ValueError("Fecha o hora con formato inválido")

        for cita in self.agenda.obtener_citas():
            if cita.id_cita == id_cita:
                if validaciones.existe_conflicto(self.agenda, nueva_fecha, nueva_hora):
                    raise ValueError("Ya existe una cita en esa fecha y hora")
                cita.actualizar_fecha_hora(nueva_fecha, nueva_hora)
                return True
        raise ValueError("La cita no existe")
