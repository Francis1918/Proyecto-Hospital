from typing import List, Tuple
from datetime import datetime


class ConsultaExternaController:
    def __init__(self):
        # Agenda sincronizada con los datos de ejemplo de PacienteController
        self._agenda_hoy = [
            {
                "id_cita": "CE-2025-001", 
                "cc": "1234567890", 
                "paciente": "Juan Carlos Pérez García", 
                "hora": "08:00", 
                "estado": "Pendiente"
            },
            {
                "id_cita": "CE-2025-002", 
                "cc": "0987654321", 
                "paciente": "María Elena González López", 
                "hora": "09:30", 
                "estado": "Pendiente"
            },
            {
                "id_cita": "CE-2025-003", 
                "cc": "1122334455", 
                "paciente": "Carlos Alberto Rodríguez Martínez", 
                "hora": "10:15", 
                "estado": "Pendiente"
            }
        ]
        self._consultas_realizadas = {}

    def consultar_agenda(self) -> List[dict]:
        """Caso de uso: consultarAgenda"""
        return self._agenda_hoy

    def registrar_anamnesis(self, id_cita: str, datos: dict) -> tuple[bool, str]:
        """
        Caso de uso: registrarAnamnesis con control de datos erróneos.
        """
        if not id_cita:
            return False, "Debe seleccionar una cita activa de la tabla."

        try:
            # 1. Intento de conversión para detectar letras donde debe haber números
            peso = float(datos.get('peso', 0))
            talla = float(datos.get('talla', 0))
            presion = str(datos.get('presion', '')).strip()
            motivo = str(datos.get('motivo', '')).strip()

            # 2. Validación de lógica física y clínica
            if peso <= 0 or peso > 500:
                return False, f"Peso inválido ({peso} kg). Debe ser un valor positivo real."
            
            if talla <= 0.3 or talla > 2.50:
                return False, f"Talla inválida ({talla} m). Ingrese valores entre 0.30 y 2.50."

            if not presion or "/" not in presion:
                return False, "Formato de presión arterial incorrecto (ej: 120/80)."

            if len(motivo) < 5:
                return False, "El motivo de consulta es demasiado breve o está vacío."

            # 3. Guardado si los datos son lógicos
            if id_cita not in self._consultas_realizadas:
                self._consultas_realizadas[id_cita] = {}
            
            self._consultas_realizadas[id_cita]['anamnesis'] = {
                'peso': peso,
                'talla': talla,
                'presion': presion,
                'motivo': motivo,
                'imc': round(peso / (talla ** 2), 2)
            }

            # Actualizar estado en la agenda local
            for cita in self._agenda_hoy:
                if cita['id_cita'] == id_cita:
                    cita['estado'] = 'Triaje Completado'
            
            return True, "Anamnesis validada y registrada correctamente."

        except ValueError:
            return False, "Error de tipo: Peso y Talla deben ser números (use punto para decimales)."
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

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