from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
from .repository import repo_orden

class ConsultarOrdenDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Consultar Órdenes")

        layout = QVBoxLayout(self)
        self.id_paciente = QLineEdit()
        self.id_paciente.setPlaceholderText("ID Paciente")

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)

        btn = QPushButton("Consultar")
        btn.clicked.connect(self.consultar)

        layout.addWidget(self.id_paciente)
        layout.addWidget(btn)
        layout.addWidget(self.resultado)

    def consultar(self):
        ordenes = repo_orden.obtener_por_paciente(self.id_paciente.text())
        if not ordenes:
            self.resultado.setText("No existen órdenes.")
            return

        texto = ""
        for o in ordenes:
            texto += (
                f"ID: {o.id_orden}\n"
                f"Médico: {o.medico}\n"
                f"Descripción: {o.descripcion}\n"
                f"Estado: {o.estado}\n"
                f"Fecha: {o.fecha}\n"
                "-----------------------\n"
            )

        self.resultado.setText(texto)
