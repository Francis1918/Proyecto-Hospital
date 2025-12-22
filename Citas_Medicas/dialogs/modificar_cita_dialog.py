from datetime import date, time, timedelta

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDateEdit, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout
)

from ..citas_controller import CitasMedicasController


class ModificarCitaDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Modificar Cita Médica")
        self.setModal(True)
        self.setMinimumWidth(520)
        self._cita_codigo = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("✏️ Modificar Cita")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        form = QFormLayout()

        self.edt_codigo = QLineEdit()
        self.edt_codigo.setPlaceholderText("Ej: CM-ABC123")
        form.addRow("Código:", self.edt_codigo)

        self.lbl_info = QLabel("-")
        self.lbl_info.setWordWrap(True)
        form.addRow("Cita actual:", self.lbl_info)

        self.date_nueva = QDateEdit()
        self.date_nueva.setCalendarPopup(True)
        self.date_nueva.setMinimumDate(date.today() + timedelta(days=1))
        self.date_nueva.dateChanged.connect(self._refrescar_horas)
        form.addRow("Nueva fecha:", self.date_nueva)

        self.cmb_hora = QComboBox()
        form.addRow("Nueva hora:", self.cmb_hora)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cargar = QPushButton("Cargar")
        btn_cargar.clicked.connect(self._cargar)
        btns.addWidget(btn_cargar)

        self.btn_guardar = QPushButton("Guardar cambios")
        self.btn_guardar.clicked.connect(self._guardar)
        self.btn_guardar.setEnabled(False)
        btns.addWidget(self.btn_guardar)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.reject)
        btns.addWidget(btn_cerrar)

        layout.addLayout(btns)

    def _cargar(self):
        codigo = (self.edt_codigo.text() or "").strip()
        cita = self.controller.consultar_cita_por_codigo(codigo)
        if not cita:
            QMessageBox.information(self, "Cita", "No se encontró la cita.")
            self.lbl_info.setText("-")
            self.btn_guardar.setEnabled(False)
            self._cita_codigo = None
            return

        self._cita_codigo = cita.codigo
        self.lbl_info.setText(
            f"{cita.nombre_paciente} | {cita.especialidad} | {cita.medico} | "
            f"{cita.fecha.isoformat()} {cita.hora.strftime('%H:%M')} | Estado: {cita.estado}"
        )

        self.date_nueva.setDate(cita.fecha)
        self._refrescar_horas()

        idx = self.cmb_hora.findText(cita.hora.strftime("%H:%M"))
        if idx >= 0:
            self.cmb_hora.setCurrentIndex(idx)

        self.btn_guardar.setEnabled(True)

    def _refrescar_horas(self):
        if not self._cita_codigo:
            return
        cita = self.controller.consultar_cita_por_codigo(self._cita_codigo)
        if not cita:
            return

        qd = self.date_nueva.date()
        nueva_fecha = date(qd.year(), qd.month(), qd.day())

        self.cmb_hora.clear()
        horas = self.controller.obtener_horarios_disponibles(cita.medico, nueva_fecha)

        # permitir la hora original si misma fecha
        if nueva_fecha == cita.fecha and cita.hora not in horas:
            horas = sorted(horas + [cita.hora])

        for h in horas:
            self.cmb_hora.addItem(h.strftime("%H:%M"), h)

        if not horas:
            self.cmb_hora.addItem("(Sin horarios disponibles)", None)

    def _guardar(self):
        if not self._cita_codigo:
            return

        qd = self.date_nueva.date()
        nueva_fecha = date(qd.year(), qd.month(), qd.day())
        if nueva_fecha <= date.today():
            QMessageBox.warning(
                self, 
                "Fecha inválida", 
                "La fecha de la cita debe ser posterior al día de hoy."
            )
            return

        hora_data = self.cmb_hora.currentData()
        if not isinstance(hora_data, time):
            QMessageBox.warning(self, "Horario", "Seleccione un horario válido.")
            return

        ok, msg, _ = self.controller.modificar_cita(self._cita_codigo, nueva_fecha, hora_data)
        if not ok:
            QMessageBox.warning(self, "No se pudo modificar", msg)
            return

        QMessageBox.information(self, "Cita", msg)
        self.accept()
