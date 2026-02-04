from datetime import date, timedelta, time, datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDateEdit, QDialog, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout
)

from Pacientes.dialogs import RegistrarPacienteDialog
from ..citas_controller import CitasMedicasController
from ..validaciones import ValidacionesCitas
from ..dialogos_estilizados import (
    mostrar_error_cedula_invalida,
    mostrar_error_paciente_no_encontrado,
    mostrar_error_sin_horarios,
    mostrar_error_horario_ocupado,
    mostrar_error_fecha_invalida,
    mostrar_exito_cita_registrada,
    mostrar_error_lista_validacion
)
from core.theme import get_sheet, AppPalette


class SolicitarCitaDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Solicitar / Agendar Cita Médica")
        self.setModal(True)
        self.setMinimumWidth(520)
        # Aplicar tema consistente
        self.setStyleSheet(get_sheet())
        self._paciente_validado = False
        
        self._init_ui()
        ##self.cargar_especialidades()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        titulo = QLabel("📅 Solicitar Cita Médica")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        form = QFormLayout()

        self.edt_cc = QLineEdit()
        self.edt_cc.setPlaceholderText("Ingrese cédula (10 dígitos)")
        form.addRow("Cédula:", self.edt_cc)

        self.lbl_paciente = QLabel("-")
        self.lbl_paciente.setStyleSheet("color: #2d3748;")
        form.addRow("Paciente:", self.lbl_paciente)

        self.cmb_especialidad = QComboBox()
        self.cmb_especialidad.addItems(self.controller.obtener_especialidades())
        self.cmb_especialidad.currentTextChanged.connect(self._on_especialidad_change)
        form.addRow("Especialidad:", self.cmb_especialidad)

        self.cmb_medico = QComboBox()
        self.cmb_medico.currentTextChanged.connect(self._on_medico_or_fecha_change)
        form.addRow("Médico:", self.cmb_medico)

        self.date_fecha = QDateEdit()
        self.date_fecha.setCalendarPopup(True)
        self.date_fecha.setDate(date.today())
        self.date_fecha.setMinimumDate(date.today())
        self.date_fecha.dateChanged.connect(self._on_medico_or_fecha_change)
        form.addRow("Fecha:", self.date_fecha)

        self.cmb_hora = QComboBox()
        form.addRow("Hora:", self.cmb_hora)

        layout.addLayout(form)

        btns = QHBoxLayout()
        self.btn_validar = QPushButton("Validar paciente")
        self.btn_validar.clicked.connect(self._validar_paciente)
        btns.addWidget(self.btn_validar)

        self.btn_agendar = QPushButton("Confirmar cita")
        self.btn_agendar.clicked.connect(self._confirmar)
        self.btn_agendar.setEnabled(False)
        btns.addWidget(self.btn_agendar)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btns.addWidget(btn_cancelar)

        layout.addLayout(btns)

        self._on_especialidad_change(self.cmb_especialidad.currentText())
        self.edt_cc.textChanged.connect(self._reset_validacion)

    def _on_especialidad_change(self, especialidad: str):
        """Actualiza la lista de médicos y limpia el flujo de selección."""
        self.cmb_medico.blockSignals(True)
        self.cmb_medico.clear()
        
        if especialidad:
            # El controlador devuelve: [(id, "Nombre"), (id, "Nombre")]
            medicos_raw = self.controller.obtener_medicos_por_especialidad(especialidad)
            
            if medicos_raw:
                for id_medico, nombre_completo in medicos_raw:
                    # Guardamos el ID como 'Data' y el nombre como 'Text'
                    self.cmb_medico.addItem(nombre_completo, id_medico)
            else:
                self.cmb_medico.addItem("No hay médicos disponibles", None)
        
        self.cmb_medico.blockSignals(False)
        self._on_medico_or_fecha_change()
        self.btn_agendar.setEnabled(False)
        
        
    def _on_medico_or_fecha_change(self):
        """Actualiza las horas disponibles aplicando restricciones de negocio y SQLite."""
        # Obtenemos el ID que guardamos en currentData
        id_medico = self.cmb_medico.currentData()
        
        if id_medico is None:
            self.cmb_hora.clear()
            self.btn_agendar.setEnabled(False)
            return

        qd = self.date_fecha.date()
        fecha = date(qd.year(), qd.month(), qd.day())
        self.cmb_hora.clear()

        # Enviamos el ID (int) al controlador, no el texto
        horas = self.controller.obtener_horarios_disponibles(id_medico, fecha)

        for h in horas:
            self.cmb_hora.addItem(h.strftime("%H:%M"), h)

        if not horas:
            self.cmb_hora.addItem("(Sin cupos)", None)
            self.btn_agendar.setEnabled(False)
        else:
            # Si el paciente ya está validado y hay horas, habilitamos confirmar
            if self._paciente_validado:
                self.btn_agendar.setEnabled(True)
            else:
                self.btn_agendar.setEnabled(False)
                # Solo mostrar el aviso si el campo de cédula no está vacío
                if self.edt_cc.text().strip():
                    self.lbl_paciente.setText("⚠️ Valide al paciente")
                    self.lbl_paciente.setStyleSheet("color: orange;")

    def _validar_paciente(self):
        """Valida formato de cédula, existencia en DB y habilita el agendamiento."""
        cc = (self.edt_cc.text() or "").strip()
        
        # 1. RESTRICCIÓN: Validación de cédula ecuatoriana
        ok, msg = self.controller.validar_formato_cedula(cc)
        if not ok:
            # Mostrar error con estilo UI
            mostrar_error_cedula_invalida(cc, msg, self)
            self.lbl_paciente.setText("❌ Cédula incorrecta")
            self.lbl_paciente.setStyleSheet(f"color: {AppPalette.Danger};")
            self.btn_agendar.setEnabled(False)
            return

        # 2. BÚSQUEDA EN SQLite
        paciente = self.controller.pacientes.consultar_paciente(cc)
        
        if not paciente:
            # Usar el nuevo diálogo estilizado
            resp = mostrar_error_paciente_no_encontrado(cc, self)
            
            if resp == QMessageBox.Yes:
                # Abrimos el diálogo que importaste al inicio
                dlg = RegistrarPacienteDialog(self.controller.pacientes, self)
                dlg.exec()
                # Re-intentamos consultar después del registro
                paciente = self.controller.pacientes.consultar_paciente(cc)

        # 3. RESTRICCIÓN: Verificación final de carga
        if not paciente:
            self.lbl_paciente.setText("❌ No se validó el paciente")
            self.lbl_paciente.setStyleSheet(f"color: {AppPalette.Danger};")
            self.btn_agendar.setEnabled(False)
            return

        # 4. ÉXITO: Actualizamos UI con datos de la DB
        # Ajustado a nombres/apellidos según la estructura estándar
        nombre_completo = f"{paciente.nombre} {paciente.apellido}"
        self.lbl_paciente.setText(f"✅ {nombre_completo}")
        self.lbl_paciente.setStyleSheet(f"color: {AppPalette.Success}; font-weight: bold;")
        self._paciente_validado = True # <--- Marcamos como validado
        
        hora_valida = self.cmb_hora.currentData() is not None
        if hora_valida:
            self.btn_agendar.setEnabled(True)
        else:
            # Mostrar advertencia con estilo
            from ..dialogos_estilizados import DialogoAdvertencia
            dlg = DialogoAdvertencia(
                "⚠️ Seleccione Horario",
                "Paciente validado, pero debe seleccionar un horario disponible.",
                self
            )
            dlg.exec()
            self.btn_agendar.setEnabled(False)
            
    def _confirmar(self):
        """Finaliza el proceso, aplica restricciones finales y guarda en SQLite."""
        cc = (self.edt_cc.text() or "").strip()
        id_medico = self.cmb_medico.currentData() # Obtenemos el ID (int)
        hora_data = self.cmb_hora.currentData()
        
        qd = self.date_fecha.date()
        fecha = date(qd.year(), qd.month(), qd.day())

        # Validaciones de seguridad adicionales
        if id_medico is None:
            mostrar_error_lista_validacion(
                "❌ Error de Validación",
                ["Debe seleccionar un médico válido."],
                self
            )
            return
        
        if not isinstance(hora_data, time):
            mostrar_error_lista_validacion(
                "❌ Error de Validación",
                ["Debe seleccionar una hora válida."],
                self
            )
            return

        # Ahora pasamos id_medico (el controlador lo espera así)
        ok, msg, cita = self.controller.solicitar_cita(
            cc=cc, 
            id_medico=id_medico, 
            fecha=fecha, 
            hora=hora_data
        )

        if not ok:
            # Si el controlador detecta un choque de último segundo en la DB
            mostrar_error_lista_validacion(
                "❌ Error al Agendar",
                [msg],
                self
            )
            return

        # 5. COMPROBANTE: Usar el nuevo diálogo estilizado
        mostrar_exito_cita_registrada(
            codigo=cita.codigo,
            paciente=cita.nombre_paciente,
            medico=cita.medico,
            fecha=cita.fecha.strftime('%d/%m/%Y'),
            hora=cita.hora.strftime('%H:%M'),
            parent=self
        )
        
        # Cerramos el diálogo con éxito
        self.accept()

    def _reset_validacion(self):
        """Si el usuario cambia la cédula, invalidamos el estado previo."""
        self._paciente_validado = False
        self.btn_agendar.setEnabled(False)
        self.lbl_paciente.setText("-")
        self.lbl_paciente.setStyleSheet("color: #2d3748;")