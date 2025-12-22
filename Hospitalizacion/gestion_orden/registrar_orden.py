from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout
)
from datetime import datetime
from .models import OrdenMedica
from .repository import orden_repo

# reutiliza pacientes del repositorio de hospitalización
from Hospitalizacion.camas_y_salas.repository import repo as hosp_repo

class RegistrarOrdenDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Orden Médica")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        self.id_paciente = QLineEdit()
        self.descripcion = QLineEdit()
        self.medico = QLineEdit()

        layout.addRow("ID Paciente", self.id_paciente)
        layout.addRow("Descripción de la orden", self.descripcion)
        layout.addRow("Médico responsable", self.medico)

        btns = QHBoxLayout()
        btn_ok = QPushButton("Registrar")
        btn_cancel = QPushButton("Cancelar")

        btn_ok.clicked.connect(self.registrar)
        btn_cancel.clicked.connect(self.reject)

        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addRow(btns)

    def registrar(self):
        pid = self.id_paciente.text().strip()
        desc = self.descripcion.text().strip()
        medico = self.medico.text().strip()

        if not pid or not desc or not medico:
            QMessageBox.critical(self, "Error", "Todos los campos son obligatorios")
            return

        paciente = hosp_repo.pacientes.get(pid)
        if not paciente or paciente.estado != "hospitalizado":
            QMessageBox.critical(
                self,
                "Error",
                "El paciente no está hospitalizado o no existe"
            )
            return

        orden = OrdenMedica(
            id_orden=f"O-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            id_paciente=pid,
            descripcion=desc,
            fecha=datetime.now(),
            medico=medico
        )

        orden_repo.registrar_orden(orden)
        QMessageBox.information(self, "Éxito", "Orden médica registrada")
        self.accept()
