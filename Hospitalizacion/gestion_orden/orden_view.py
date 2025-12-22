from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

from .registrar_orden import RegistrarOrdenDialog
from .consultar_orden import ConsultarOrdenDialog

class GestionOrdenView(QMainWindow):
    def __init__(self, rol: str, parent=None):
        super().__init__(parent)
        self.rol = rol
        self.padre = parent
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gestión de Orden Médica")
        self.setMinimumSize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        titulo = QLabel("Gestión de Orden Médica")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(titulo)

        btn_registrar = QPushButton("Registrar Orden Médica")
        btn_consultar = QPushButton("Consultar Órdenes")

        btn_registrar.clicked.connect(self.registrar_orden)
        btn_consultar.clicked.connect(self.consultar_orden)

        layout.addWidget(btn_registrar)
        layout.addWidget(btn_consultar)

        btn_volver = QPushButton("Regresar")
        btn_volver.clicked.connect(self.volver)
        layout.addWidget(btn_volver)

    def registrar_orden(self):
        if self.rol != "MEDICO":
            return
        dlg = RegistrarOrdenDialog(self)
        dlg.exec()

    def consultar_orden(self):
        dlg = ConsultarOrdenDialog(self)
        dlg.exec()

    def volver(self):
        if self.padre:
            self.padre.show()
        self.close()
