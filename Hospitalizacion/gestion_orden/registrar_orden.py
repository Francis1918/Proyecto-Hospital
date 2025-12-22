from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit,
    QPushButton, QMessageBox
)
from datetime import datetime
from .models import OrdenMedica
from .repository import repo_orden

class RegistrarOrdenDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Orden Médica")

        layout = QFormLayout(self)
        self.id_paciente = QLineEdit()
        self.medico = QLineEdit()
        self.descripcion = QLineEdit()

        layout.addRow("ID Paciente", self.id_paciente)
        layout.addRow("Médico", self.medico)
        layout.addRow("Descripción", self.descripcion)

        btn = QPushButton("Registrar")
        btn.clicked.connect(self.registrar)
        layout.addWidget(btn)

    def registrar(self):
        if not self.id_paciente.text():
            QMessageBox.warning(self, "Error", "Campos obligatorios")
            return

        orden = OrdenMedica(
            id_orden=f"ORD-{datetime.now().strftime('%H%M%S')}",
            id_paciente=self.id_paciente.text(),
            medico=self.medico.text(),
            descripcion=self.descripcion.text(),
            fecha=datetime.now()
        )

        repo_orden.registrar(orden)
        QMessageBox.information(self, "OK", "Orden registrada")
        self.accept()
