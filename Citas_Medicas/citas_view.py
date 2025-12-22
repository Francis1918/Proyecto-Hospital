from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt

from .citas_controller import CitasMedicasController


class CitasMedicasView(QMainWindow):
    def __init__(self, controller: CitasMedicasController = None):
        super().__init__()
        self.controller = controller or CitasMedicasController()
        self.init_ui()

    def get_styles(self):
        return """
        QMainWindow { background-color: #e8f4fc; }
        QWidget#central { background-color: #e8f4fc; }
        QLabel#titulo { color: #1a365d; font-size: 30px; font-weight: bold; padding: 20px; }
        QFrame#menu_container { background-color: #e8f4fc; padding: 20px; }
        QPushButton.menu_btn {
            background-color: #3182ce;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 20px;
            font-size: 15px;
            font-weight: bold;
            min-height: 70px;
            min-width: 220px;
        }
        QPushButton.menu_btn:hover { background-color: #2c5282; }
        QPushButton.menu_btn:pressed { background-color: #1a365d; }

        QPushButton#btn_salir {
            background-color: #3182ce;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 20px;
            font-size: 15px;
            font-weight: bold;
            min-height: 70px;
            min-width: 220px;
        }
        QPushButton#btn_salir:hover { background-color: #2c5282; }
        QPushButton#btn_salir:pressed { background-color: #1a365d; }
        """

    def init_ui(self):
        self.setWindowTitle("Sistema de Gestión Clínica - Citas Médicas")
        self.setMinimumSize(1000, 650)
        self.setStyleSheet(self.get_styles())

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(20)

        titulo = QLabel("📅 Módulo de Citas Médicas")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        menu = self.crear_menu_botones()
        layout.addWidget(menu)
        layout.addStretch()

    def crear_menu_botones(self):
        container = QFrame()
        container.setObjectName("menu_container")
        grid = QGridLayout(container)
        grid.setSpacing(18)
        grid.setContentsMargins(20, 20, 20, 20)

        botones = [
            ("Solicitar Cita", self.abrir_solicitar),
            ("Consultar Cita", self.abrir_consultar),
            ("Modificar Cita", self.abrir_modificar),
            ("Cancelar Cita", self.abrir_eliminar),
            ("Consultar Agenda", self.abrir_agenda),
            ("Registrar Estado (Recepción)", self.abrir_estado),
            ("Historial Notificaciones", self.abrir_notificaciones),
            ("Registrar Agenda Médico", self.abrir_registrar_agenda),
            ("Salir", self.close),
        ]

        for i, (texto, fn) in enumerate(botones):
            btn = QPushButton(texto)
            if texto == "Salir":
                btn.setObjectName("btn_salir")
            else:
                btn.setProperty("class", "menu_btn")

            btn.clicked.connect(fn)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            row = i // 2
            col = i % 2
            grid.addWidget(btn, row, col)

        return container

    def abrir_solicitar(self):
        from .dialogs import SolicitarCitaDialog
        dlg = SolicitarCitaDialog(self.controller, self)
        dlg.exec()

    def abrir_consultar(self):
        from .dialogs import ConsultarCitaDialog
        dlg = ConsultarCitaDialog(self.controller, self)
        dlg.exec()

    def abrir_modificar(self):
        from .dialogs import ModificarCitaDialog
        dlg = ModificarCitaDialog(self.controller, self)
        dlg.exec()

    def abrir_eliminar(self):
        from .dialogs import EliminarCitaDialog
        dlg = EliminarCitaDialog(self.controller, self)
        dlg.exec()

    def abrir_agenda(self):
        from .dialogs import ConsultarAgendaDialog
        dlg = ConsultarAgendaDialog(self.controller, self)
        dlg.exec()

    def abrir_estado(self):
        from .dialogs import RegistrarEstadoDialog
        dlg = RegistrarEstadoDialog(self.controller, self)
        dlg.exec()

    def abrir_notificaciones(self):
        from .dialogs import HistorialNotificacionesDialog
        dlg = HistorialNotificacionesDialog(self.controller, self)
        dlg.exec()

    def abrir_registrar_agenda(self):
        from .dialogs import RegistrarAgendaDialog
        dlg = RegistrarAgendaDialog(self.controller, self)
        dlg.exec()
