from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout
)

from ..citas_controller import CitasMedicasController


class ConsultarCitaDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Consultar Cita Médica")
        self.setModal(True)
        self.setMinimumWidth(720)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("🔎 Consultar Cita")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        form = QFormLayout()
        self.edt_codigo = QLineEdit()
        self.edt_codigo.setPlaceholderText("Ej: CM-ABC123")
        form.addRow("Código de cita:", self.edt_codigo)

        self.edt_cc = QLineEdit()
        self.edt_cc.setPlaceholderText("(Opcional) Cédula del paciente")
        form.addRow("Cédula:", self.edt_cc)
        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self._buscar)
        btns.addWidget(btn_buscar)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.reject)
        btns.addWidget(btn_cerrar)

        layout.addLayout(btns)

        self.tabla = QTableWidget(0, 7)
        self.tabla.setHorizontalHeaderLabels(
            ["Código", "Paciente", "Especialidad", "Médico", "Fecha", "Hora", "Estado"]
        )
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tabla)

    def _buscar(self):
        codigo = (self.edt_codigo.text() or "").strip()
        cc = (self.edt_cc.text() or "").strip()

        citas = []
        if codigo:
            c = self.controller.consultar_cita_por_codigo(codigo)
            if c:
                citas = [c]
        elif cc:
            ok, msg = self.controller.validar_formato_cedula(cc)
            if not ok:
                QMessageBox.warning(self, "Cédula inválida", msg)
                return
            citas = self.controller.consultar_citas_por_paciente(cc)
        else:
            QMessageBox.information(self, "Buscar", "Ingrese un código o una cédula para buscar.")
            return

        self.tabla.setRowCount(0)
        if not citas:
            QMessageBox.information(self, "Sin resultados", "No se encontraron citas.")
            return

        for c in citas:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            vals = [
                c.codigo, c.nombre_paciente, c.especialidad, c.medico,
                c.fecha.isoformat(), c.hora.strftime("%H:%M"), c.estado
            ]
            for col, v in enumerate(vals):
                self.tabla.setItem(row, col, QTableWidgetItem(str(v)))
