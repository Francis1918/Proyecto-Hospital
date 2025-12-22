from datetime import date, timedelta, time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDateEdit, QDialog, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout
)

from Pacientes.dialogs import RegistrarPacienteDialog
from ..citas_controller import CitasMedicasController


class SolicitarCitaDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Solicitar / Agendar Cita Médica")
        self.setModal(True)
        self.setMinimumWidth(520)
        self._init_ui()

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
        self.date_fecha.setDate(date.today() + timedelta(days=1))
        self.date_fecha.setMinimumDate(date.today() + timedelta(days=1))
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

    def _on_especialidad_change(self, especialidad: str):
        self.cmb_medico.clear()
        medicos = self.controller.obtener_medicos_por_especialidad(especialidad)
        self.cmb_medico.addItems(medicos)
        self._on_medico_or_fecha_change()

    def _on_medico_or_fecha_change(self):
        medico = self.cmb_medico.currentText().strip()
        qd = self.date_fecha.date()
        fecha = date(qd.year(), qd.month(), qd.day())

        self.cmb_hora.clear()
        if not medico:
            return

        horas = self.controller.obtener_horarios_disponibles(medico, fecha)
        for h in horas:
            self.cmb_hora.addItem(h.strftime("%H:%M"), h)

        if not horas:
            self.cmb_hora.addItem("(Sin horarios disponibles)", None)

    def _validar_paciente(self):
        cc = (self.edt_cc.text() or "").strip()
        ok, msg = self.controller.validar_formato_cedula(cc)
        if not ok:
            QMessageBox.warning(self, "Cédula inválida", msg)
            self.lbl_paciente.setText("-")
            self.btn_agendar.setEnabled(False)
            return

        paciente = self.controller.pacientes.consultar_paciente(cc)
        if not paciente:
            resp = QMessageBox.question(
                self,
                "Paciente no registrado",
                "Paciente no registrado en la base de datos.\n\n¿Desea registrarlo ahora?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if resp == QMessageBox.StandardButton.Yes:
                dlg = RegistrarPacienteDialog(self.controller.pacientes, self)
                dlg.exec()
                paciente = self.controller.pacientes.consultar_paciente(cc)

        if not paciente:
            QMessageBox.information(self, "Paciente", "No se pudo validar/registrar el paciente.")
            self.lbl_paciente.setText("-")
            self.btn_agendar.setEnabled(False)
            return

        self.lbl_paciente.setText(f"{paciente.nombre} {paciente.apellido}")
        self.btn_agendar.setEnabled(True)
        QMessageBox.information(self, "Paciente", "Paciente validado correctamente.")

    def _confirmar(self):
        cc = (self.edt_cc.text() or "").strip()
        especialidad = self.cmb_especialidad.currentText().strip()
        medico = self.cmb_medico.currentText().strip()

        qd = self.date_fecha.date()
        fecha = date(qd.year(), qd.month(), qd.day())
        if fecha <= date.today():
            QMessageBox.warning(
                self, 
                "Fecha inválida", 
                "La fecha de la cita debe ser posterior al día de hoy."
            )
            return
        
        hora_data = self.cmb_hora.currentData()
        if not isinstance(hora_data, time):
            QMessageBox.warning(self, "Sin horario", "Seleccione un horario válido.")
            return

        ok, msg, cita = self.controller.solicitar_cita(
            cc=cc, especialidad=especialidad, medico=medico, fecha=fecha, hora=hora_data
        )

        if not ok:
            QMessageBox.warning(self, "No se pudo agendar", msg)
            return

        comprobante = (
            "✅ Cita registrada\n\n"
            f"Especialidad: {cita.especialidad}\n"
            f"Médico: {cita.medico}\n"
            f"Fecha: {cita.fecha.isoformat()}\n"
            f"Hora: {cita.hora.strftime('%H:%M')}\n"
            f"Consultorio: {cita.consultorio}\n"
            f"Código: {cita.codigo}\n\n"
            "Solicitud de cita médica enviada exitosamente y en proceso de confirmación."
        )
        QMessageBox.information(self, "Comprobante", comprobante)
        self.accept()
