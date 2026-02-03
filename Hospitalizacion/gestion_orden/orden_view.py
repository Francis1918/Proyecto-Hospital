from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QMessageBox,
    QWidget, QVBoxLayout, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt

from .registrar_orden import RegistrarOrdenDialog
from .consultar_orden import ConsultarOrdenDialog
from .actualizar_orden import ActualizarOrdenDialog
from .anular_orden import AnularOrdenDialog

class GestionOrdenView(QMainWindow):
    def __init__(self, rol, parent=None):
        super().__init__(parent)
        self.rol = rol
        self.parent_view = parent
        self.init_ui()

    def get_styles(self):
        return """
            QMainWindow { background-color: #e8f4fc; }
            QWidget#central { background-color: #e8f4fc; }
            QLabel#titulo { color: #1a365d; font-size: 26px; font-weight: bold; padding: 12px; }
            QFrame#menu_container { background-color: rgba(255,255,255,0.95); border-radius: 12px; padding: 16px; }
            QPushButton.menu_btn { background-color: #3182ce; color: white; border: none; border-radius: 8px; padding: 16px; font-size: 14px; font-weight: bold; min-height: 56px; min-width: 220px; }
            QPushButton.menu_btn:hover { background-color: #2c5282; }
            QPushButton.menu_btn:pressed { background-color: #1a365d; }
            /* Botón volver eliminado en versión embebida */
        """

    def init_ui(self):
        self.setWindowTitle("Gestión de Orden Médica")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(self.get_styles())

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 20, 40, 20)

        titulo = QLabel("Gestión de Orden Médica")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        container = QFrame()
        container.setObjectName("menu_container")
        layout.addWidget(container)
        
        # Grid para los botones (2x2)
        grid = QGridLayout(container)
        grid.setSpacing(16)
        grid.setContentsMargins(16, 16, 16, 16)

        # 1. Registrar
        self.btn_registrar = QPushButton("Registrar orden de hospitalización")
        self.btn_registrar.setProperty("class", "menu_btn")
        self.btn_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_registrar.clicked.connect(self.registrar)
        grid.addWidget(self.btn_registrar, 0, 0)

        # 2. Consultar
        self.btn_consultar = QPushButton("Consultar orden de hospitalización")
        self.btn_consultar.setProperty("class", "menu_btn")
        self.btn_consultar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_consultar.clicked.connect(self.consultar)
        grid.addWidget(self.btn_consultar, 0, 1)

        # 3. Actualizar
        self.btn_actualizar = QPushButton("Actualizar orden de hospitalización")
        self.btn_actualizar.setProperty("class", "menu_btn")
        self.btn_actualizar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_actualizar.clicked.connect(self.actualizar)
        grid.addWidget(self.btn_actualizar, 1, 0)

        # 4. Anular
        self.btn_anular = QPushButton("Anular orden de hospitalización")
        self.btn_anular.setProperty("class", "menu_btn")
        self.btn_anular.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_anular.clicked.connect(self.anular)
        grid.addWidget(self.btn_anular, 1, 1)

        # Botón 'Volver' eliminado: la navegación la controla la vista padre

    def registrar(self):
        if self.rol != "MEDICO":
            QMessageBox.warning(self, "Acceso", "Solo el médico puede registrar órdenes")
            return
        RegistrarOrdenDialog(self).exec()

    def consultar(self):
        ConsultarOrdenDialog(self).exec()

    def actualizar(self):
        if self.rol != "MEDICO":
            QMessageBox.warning(self, "Acceso", "Solo el médico puede actualizar órdenes")
            return
        ActualizarOrdenDialog(self).exec()

    def anular(self):
        if self.rol != "MEDICO": # Asumimos solo médico puede anular
             QMessageBox.warning(self, "Acceso", "Solo el médico puede anular órdenes")
             return
        AnularOrdenDialog(self).exec()

