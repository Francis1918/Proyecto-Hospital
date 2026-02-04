from PyQt6.QtWidgets import QMessageBox
import sys
import os

# Añadir el directorio raíz al path para permitir importaciones absolutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import insertar_signos_vitales, obtener_signos_vitales, crear_conexion, actualizar_datos_medicos
from Pacientes.paciente_controller import PacienteController

class ConsultaExternaController:
    def __init__(self, view):
        self.view = view

    def guardar_signos_vitales(self):
        """
        Obtiene los datos de la vista, los valida y los guarda en la BD.
        """
        datos = self.view.get_valores_signos_vitales()
        cedula = datos["cedula"]
        
        if not cedula:
            QMessageBox.warning(self.view, "Error de Validación", "El campo 'Cédula' no puede estar vacío.")
            return

        # Verificar si el paciente existe
        if not self._verificar_paciente(cedula):
            # Preguntar si desea registrar al paciente
            respuesta = QMessageBox.question(
                self.view,
                "Paciente no Encontrado",
                f"No se encontró un paciente con la cédula '{cedula}'.\n\n¿Desea registrarlo ahora?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:
                # Aquí puedes abrir un diálogo para registrar el paciente
                # Por ahora solo mostramos un mensaje
                QMessageBox.information(
                    self.view,
                    "Información",
                    "Por favor, registre al paciente en el módulo de Pacientes primero."
                )
            return

        try:
            peso = float(datos["peso"])
            talla = float(datos["talla"])
            
            if peso <= 0 or talla <= 0:
                raise ValueError("Peso y talla deben ser valores positivos.")

        except (ValueError, TypeError):
            QMessageBox.warning(self.view, "Error de Formato", "Peso y Talla deben ser números válidos.")
            return
            
        presion = datos["presion"]
        motivo = datos["motivo"]

        if not presion or not motivo:
            QMessageBox.warning(self.view, "Error de Validación", "Los campos 'Presión' y 'Motivo' no pueden estar vacíos.")
            return
        
        # Insertar en la base de datos
        id_registro = insertar_signos_vitales(cedula, peso, talla, presion, motivo)

        if id_registro:
            QMessageBox.information(self.view, "Éxito", f"Signos vitales guardados correctamente con ID: {id_registro}")
            self.view.limpiar_campos_signos_vitales()
            self.cargar_signos_vitales_en_vista() # Recargar la tabla
        else:
            QMessageBox.critical(self.view, "Error de Base de Datos", "No se pudieron guardar los signos vitales.")

    def _verificar_paciente(self, cedula: str) -> bool:
        """Verifica si un paciente con la cédula dada existe en la tabla de pacientes."""
        conn = crear_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM pacientes WHERE dni = ?", (cedula,))
                existe = cursor.fetchone()
                return bool(existe)
            except Exception as e:
                print(f"Error al verificar paciente: {e}")
                return False
            finally:
                conn.close()
        return False

    def cargar_signos_vitales_en_vista(self):
        """
        Obtiene los registros de signos vitales de la BD y los carga en el Treeview de la vista.
        """
        registros = obtener_signos_vitales()
        self.view.actualizar_tabla_signos_vitales(registros)

    def consultar_historia_clinica(self, cc_paciente: str) -> str:
        """Caso de uso: consultarHistoriaClínica.

        Reutiliza la misma consulta del módulo de Pacientes y devuelve un texto
        listo para mostrar en la UI (QMessageBox).
        """

        cc_paciente = (cc_paciente or "").strip()
        if not cc_paciente:
            return "Debe ingresar la cédula del paciente."

        paciente_controller = PacienteController()

        # Validar existencia del paciente para dar un mensaje claro.
        paciente = paciente_controller.consultar_paciente(cc_paciente)
        if not paciente:
            return f"No se encontró un paciente con cédula {cc_paciente}."

        historia = paciente_controller.consultar_historia_clinica(cc_paciente)
        if not historia or not historia.get('historia_clinica'):
            return f"El paciente con cédula {cc_paciente} no tiene historia clínica registrada."

        return str(historia['historia_clinica'])

    def verificar_paciente_tiene_signos_vitales(self, cedula: str) -> tuple[bool, str]:
        """
        Verifica si el paciente existe y tiene signos vitales registrados.
        Retorna (existe: bool, mensaje: str)
        """
        conn = crear_conexion()
        if not conn:
            return False, "Error de conexión con la base de datos"
        
        try:
            cursor = conn.cursor()
            
            # Verificar si existe el paciente
            cursor.execute("SELECT 1 FROM pacientes WHERE dni = ?", (cedula,))
            paciente_existe = cursor.fetchone()
            
            if not paciente_existe:
                return False, f"No existe un paciente con cédula {cedula}"
            
            # Verificar si tiene signos vitales
            cursor.execute("""
                SELECT id FROM pacienteSignosVitales 
                WHERE cedula = ? 
                ORDER BY fecha_registro DESC 
                LIMIT 1
            """, (cedula,))
            
            tiene_signos = cursor.fetchone()
            
            if not tiene_signos:
                return False, f"El paciente con cédula {cedula} no tiene signos vitales registrados. Debe registrarlos primero en la pestaña 'Signos Vitales'."
            
            return True, "OK"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()

    def registrar_diagnostico(self, cedula: str, cie10: str, observaciones: str, plan_tratamiento: str) -> tuple[bool, str]:
        """
        Registra el diagnóstico médico actualizando el registro de signos vitales más reciente.
        """
        if not cedula:
            return False, "Debe ingresar la cédula del paciente."
        
        if not cie10:
            return False, "El código CIE-10 es obligatorio para el diagnóstico."
        
        # Verificar que el paciente tenga signos vitales
        existe, mensaje = self.verificar_paciente_tiene_signos_vitales(cedula)
        if not existe:
            return False, mensaje
        
        # Actualizar los datos médicos
        exito = actualizar_datos_medicos(cedula, cie10, observaciones, plan_tratamiento)
        
        if exito:
            return True, "Diagnóstico y plan de tratamiento registrados correctamente."
        else:
            return False, "Error al registrar el diagnóstico en la base de datos."

    def emitir_receta(self, id_cita: str, receta_datos: dict, ordenes_extra: list) -> tuple[bool, str]:
        """Caso de uso: emitirReceta y sus <<extend>>"""
        if not id_cita:
            return False, "Debe registrar un diagnóstico antes de emitir la receta."

        # Aquí iría la lógica para emitir la receta
        print(f"Receta emitida para cita {id_cita}: {receta_datos}")
        
        res = "Receta emitida."
        if ordenes_extra:
            res += f" Se generaron pedidos de: {', '.join(ordenes_extra)}"
        return True, res