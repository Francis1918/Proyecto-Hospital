from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QVBoxLayout
)

from ..citas_controller import CitasMedicasController
from core.theme import get_sheet


class EliminarCitaDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Cancelar Cita Médica")
        self.setModal(True)
        self.setMinimumWidth(520)
        # Aplicar hoja de estilos global para tema consistente
        self.setStyleSheet(get_sheet())
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("🗑️ Cancelar Cita")
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
        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cargar = QPushButton("Cargar")
        btn_cargar.clicked.connect(self._cargar)
        btns.addWidget(btn_cargar)

        btn_cancelar = QPushButton("Cancelar Cita")
        btn_cancelar.clicked.connect(self._cancelar)
        btns.addWidget(btn_cancelar)

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
            return

        self.lbl_info.setText(
            f"{cita.nombre_paciente} | {cita.especialidad} | {cita.medico} | "
            f"{cita.fecha.isoformat()} {cita.hora.strftime('%H:%M')} | Estado: {cita.estado}"
        )

    def _cancelar(self):
        codigo = (self.edt_codigo.text() or "").strip()
        cita = self.controller.consultar_cita_por_codigo(codigo)
        if not cita:
            QMessageBox.warning(self, "Cita", "No se encontró la cita.")
            return

        resp = QMessageBox.question(
            self, "Confirmar", "¿Seguro que desea cancelar esta cita?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if resp != QMessageBox.StandardButton.Yes:
            return

        ok, msg = self.controller.cancelar_cita(codigo)
        if not ok:
            QMessageBox.warning(self, "No se pudo cancelar", msg)
            return

        QMessageBox.information(self, "Cita", msg)
        self.accept()
