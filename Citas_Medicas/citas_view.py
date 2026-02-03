from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLabel, QFrame, QHBoxLayout
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
        QMainWindow { background-color: #f0f4f8; }
        QLabel#titulo { 
            color: #2c3e50; 
            font-size: 32px; 
            font-weight: bold; 
            margin-bottom: 20px;
        }
        QFrame#container_principal {
            background-color: white;
            border-radius: 20px;
            border: 1px solid #d1d9e6;
        }
        QPushButton.menu_btn {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 15px;
            font-size: 16px;
            font-weight: bold;
            min-height: 80px;
        }
        QPushButton.menu_btn:hover { background-color: #2980b9; }
        QPushButton.menu_btn:pressed { background-color: #21618c; }

        QPushButton#btn_salir {
            background-color: #e74c3c;
            color: white;
            border-radius: 12px;
            padding: 10px;
            font-size: 15px;
            font-weight: bold;
            min-height: 50px;
            min-width: 150px;
        }
        QPushButton#btn_salir:hover { background-color: #c0392b; }
        """

    def init_ui(self):
        self.setWindowTitle("Gestión de Citas Médicas")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(self.get_styles())

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(50, 40, 50, 40)

        # Título
        titulo = QLabel("📅 Módulo de Citas Médicas")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(titulo)

        # Contenedor de botones (Grid)
        container = QFrame()
        container.setObjectName("container_principal")
        grid = QGridLayout(container)
        grid.setSpacing(25)
        grid.setContentsMargins(30, 30, 30, 30)

        # Lista de botones simplificada (Quitamos los 3 que pediste)
        botones_principales = [
            ("Solicitar Cita", "➕", self.abrir_solicitar),
            ("Consultar Cita", "🔍", self.abrir_consultar),
            ("Consultar Agenda", "🗓️", self.abrir_agenda),
            ("Historial Notificaciones", "📩", self.abrir_notificaciones),
            ("Registrar Agenda Médico", "🧩", self.abrir_registrar_agenda),
        ]

        for i, (texto, icono, fn) in enumerate(botones_principales):
            btn = QPushButton(f"{icono}\n{texto}")
            btn.setProperty("class", "menu_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(fn)
            
            # Acomodar en 2 columnas
            row = i // 2
            col = i % 2
            grid.addWidget(btn, row, col)

        main_layout.addWidget(container)

        # Botón Salir abajo centrado
        footer_layout = QHBoxLayout()
        btn_salir = QPushButton("Cerrar Módulo")
        btn_salir.setObjectName("btn_salir")
        btn_salir.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_salir.clicked.connect(self.close)
        
        footer_layout.addStretch()
        footer_layout.addWidget(btn_salir)
        footer_layout.addStretch()
        
        main_layout.addLayout(footer_layout)

    # --- Métodos de apertura (Se mantienen igual) ---
    def abrir_solicitar(self):
        from .dialogs import SolicitarCitaDialog
        SolicitarCitaDialog(self.controller, self).exec()

    def abrir_consultar(self):
        from .dialogs import ConsultarCitaDialog
        ConsultarCitaDialog(self.controller, self).exec()

    def abrir_agenda(self):
        from .dialogs import ConsultarAgendaDialog
        ConsultarAgendaDialog(self.controller, self).exec()

    def abrir_notificaciones(self):
        from .dialogs import HistorialNotificacionesDialog
        HistorialNotificacionesDialog(self.controller, self).exec()

    def abrir_registrar_agenda(self):
        from .dialogs import RegistrarAgendaDialog
        RegistrarAgendaDialog(self.controller, self).exec()