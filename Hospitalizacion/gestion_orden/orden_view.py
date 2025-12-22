from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt

from .registrar_orden import RegistrarOrdenDialog
from .consultar_orden import ConsultarOrdenDialog

class GestionOrdenView(QMainWindow):
    def __init__(self, rol, parent=None):
        super().__init__(parent)
        self.rol = rol
        self.parent_view = parent
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gestión de Orden Médica")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        titulo = QLabel("Gestión de Orden Médica")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(titulo)

        btn_registrar = QPushButton("Registrar orden médica")
        btn_consultar = QPushButton("Consultar órdenes")

        btn_registrar.clicked.connect(self.registrar)
        btn_consultar.clicked.connect(self.consultar)

        layout.addWidget(btn_registrar)
        layout.addWidget(btn_consultar)

        btn_volver = QPushButton("Volver")
        btn_volver.clicked.connect(self.volver)
        layout.addWidget(btn_volver)

    def registrar(self):
        if self.rol != "MEDICO":
            QMessageBox.warning(self, "Acceso", "Solo el médico puede registrar órdenes")
            return
        RegistrarOrdenDialog(self).exec()

    def consultar(self):
        ConsultarOrdenDialog(self).exec()

    def volver(self):
        if self.parent_view:
            self.parent_view.show()
        self.close()
