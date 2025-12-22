from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
from .repository import orden_repo

class ConsultarOrdenDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Consultar Órdenes")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.id_paciente = QLineEdit()
        self.id_paciente.setPlaceholderText("ID del paciente")

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)

        btn = QPushButton("Consultar")
        btn.clicked.connect(self.consultar)

        layout.addWidget(self.id_paciente)
        layout.addWidget(btn)
        layout.addWidget(self.resultado)

    def consultar(self):
        pid = self.id_paciente.text().strip()
        ordenes = orden_repo.obtener_por_paciente(pid)

        if not ordenes:
            self.resultado.setText("No existen órdenes registradas.")
            return

        texto = ""
        for o in ordenes:
            texto += (
                f"ID: {o.id_orden}\n"
                f"Fecha: {o.fecha}\n"
                f"Médico: {o.medico}\n"
                f"Descripción: {o.descripcion}\n"
                f"{'-'*30}\n"
            )

        self.resultado.setText(texto)
