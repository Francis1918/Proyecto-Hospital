from datetime import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QTimeEdit, QVBoxLayout
)

from ..citas_controller import CitasMedicasController


class RegistrarEstadoDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Registrar Estado de Cita (Recepción)")
        self.setModal(True)
        self.setMinimumWidth(560)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("🏷️ Registrar Estado de Cita")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        form = QFormLayout()

        self.edt_codigo = QLineEdit()
        self.edt_codigo.setPlaceholderText("Ej: CM-ABC123")
        form.addRow("Código:", self.edt_codigo)

        self.lbl_info = QLabel("-")
        self.lbl_info.setWordWrap(True)
        form.addRow("Detalle:", self.lbl_info)

        self.cmb_estado = QComboBox()
        self.cmb_estado.addItems(["Asistió", "Ausente", "Tardanza"])
        form.addRow("Estado:", self.cmb_estado)

        self.time_llegada = QTimeEdit()
        self.time_llegada.setDisplayFormat("HH:mm")
        form.addRow("Hora llegada (opcional):", self.time_llegada)

        self.edt_coment = QLineEdit()
        self.edt_coment.setPlaceholderText("Comentario (opcional)")
        form.addRow("Comentario:", self.edt_coment)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cargar = QPushButton("Cargar")
        btn_cargar.clicked.connect(self._cargar)
        btns.addWidget(btn_cargar)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self._guardar)
        btns.addWidget(btn_guardar)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.reject)
        btns.addWidget(btn_cerrar)

        layout.addLayout(btns)

    def _cargar(self):
        codigo = (self.edt_codigo.text() or "").strip()
        cita = self.controller.consultar_cita_por_codigo(codigo)
        if not cita:
            QMessageBox.warning(self, "Cita", "No se encontró la cita.")
            self.lbl_info.setText("-")
            return

        self.lbl_info.setText(
            f"{cita.nombre_paciente} | {cita.especialidad} | {cita.medico} | "
            f"{cita.fecha.isoformat()} {cita.hora.strftime('%H:%M')} | Estado: {cita.estado}"
        )

    def _guardar(self):
        codigo = (self.edt_codigo.text() or "").strip()
        estado = self.cmb_estado.currentText().strip()
        comentario = (self.edt_coment.text() or "").strip()

        # hora opcional
        qt = self.time_llegada.time()
        hora_llegada = time(qt.hour(), qt.minute())

        ok, msg, _ = self.controller.registrar_estado_cita(
            codigo=codigo,
            nuevo_estado=estado,
            hora_llegada=hora_llegada,
            comentario=comentario
        )
        if not ok:
            QMessageBox.warning(self, "No se pudo registrar", msg)
            return

        QMessageBox.information(self, "Recepción", msg)
        self.accept()
