from typing import List, Optional
from datetime import datetime

class ConsultaExternaController:
    def __init__(self):
        # Almacenamiento temporal (Simulando persistencia del sistema)
        self._agenda_hoy = [
            {"id_cita": "101", "cc": "1234567890", "paciente": "Juan Pérez", "hora": "08:00", "estado": "Pendiente"},
            {"id_cita": "102", "cc": "0987654321", "paciente": "María González", "hora": "09:00", "estado": "Pendiente"}
        ]
        self._consultas_realizadas = {} # id_cita -> datos_consulta

    # --- CASOS DE USO: ENFERMERA ---
    def consultar_agenda(self) -> List[dict]:
        """Caso de uso: consultarAgenda"""
        return self._agenda_hoy

    def registrar_anamnesis(self, id_cita: str, datos: dict) -> tuple[bool, str]:
        """Caso de uso: registrarAnamnesis"""
        if not id_cita:
            return False, "Debe seleccionar una cita de la agenda."
        
        # Validar datos mínimos (Triaje)
        campos_req = ['peso', 'talla', 'presion', 'motivo']
        if not all(datos.get(k) for k in campos_req):
            return False, "Todos los campos de anamnesis son obligatorios."

        if id_cita not in self._consultas_realizadas:
            self._consultas_realizadas[id_cita] = {}
        
        self._consultas_realizadas[id_cita]['anamnesis'] = datos
        # Actualizar estado en la agenda
        for cita in self._agenda_hoy:
            if cita['id_cita'] == id_cita:
                cita['estado'] = 'Triaje Completado'
        
        return True, "Anamnesis registrada exitosamente."

    # --- CASOS DE USO: MÉDICO ---
    def consultar_historia_clinica(self, cc_paciente: str) -> str:
        """Caso de uso: consultarHistoriaClínica"""
        # Aquí normalmente se comunicaría con el PacienteController
        return f"Resumen HC para {cc_paciente}: Sin alergias conocidas. Antecedentes de asma."

    def registrar_diagnostico(self, id_cita: str, cie10: str, notas: str) -> tuple[bool, str]:
        """Caso de uso: registrarDiagnóstico"""
        if id_cita not in self._consultas_realizadas or 'anamnesis' not in self._consultas_realizadas[id_cita]:
            return False, "No se puede diagnosticar sin anamnesis previa."
        
        if not cie10:
            return False, "El código CIE-10 es obligatorio para el diagnóstico."

        self._consultas_realizadas[id_cita]['diagnostico'] = {'cie10': cie10, 'notas': notas}
        return True, "Diagnóstico registrado."

    def emitir_receta(self, id_cita: str, receta_datos: dict, ordenes_extra: list) -> tuple[bool, str]:
        """Caso de uso: emitirReceta y sus <<extend>>"""
        if 'diagnostico' not in self._consultas_realizadas.get(id_cita, {}):
            return False, "Debe registrar un diagnóstico antes de emitir la receta."

        self._consultas_realizadas[id_cita]['receta'] = receta_datos
        self._consultas_realizadas[id_cita]['ordenes_extendidas'] = ordenes_extra

        # Finalizar cita
        for cita in self._agenda_hoy:
            if cita['id_cita'] == id_cita:
                cita['estado'] = 'Atendido'
        
        res = "Receta emitida."
        if ordenes_extra:
            res += f" Se generaron pedidos de: {', '.join(ordenes_extra)}"
        return True, res