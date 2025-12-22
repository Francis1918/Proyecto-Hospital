"""Vista: menú del paciente dentro del módulo Citas_Medicas.

Se expone la clase `MenuPaciente` usada por `mainCitaMedica.py`.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt

try:
    from Citas_Medicas.views.citas.agendar_cita_view import AgendarCitaView
except Exception:
    from views.citas.agendar_cita_view import AgendarCitaView


class MenuPaciente(QMainWindow):
    """Menú para acciones del paciente — igual diseño y opciones que recepcionista."""

    def __init__(self, paciente_controller):
        super().__init__()
        self.paciente_controller = paciente_controller
        self.ventanas_abiertas = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Citas Médicas - Paciente")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(self.get_styles())

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)

        header = self.crear_header()
        layout.addWidget(header)

        menu = self.crear_menu_botones()
        layout.addWidget(menu)

        footer = self.crear_footer()
        layout.addWidget(footer)

    def get_styles(self):
        return """
            QMainWindow {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2
                );
            }
            QWidget#central {
                background: transparent;
            }
            QFrame#header {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 20px;
            }
            QFrame#menu_container {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 30px;
            }
            QLabel#titulo {
                color: #2d3748;
                font-size: 28px;
                font-weight: bold;
            }
            QLabel#subtitulo {
                color: #718096;
                font-size: 14px;
            }
            QPushButton.menu_btn {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2
                );
                color: white;
                border: none;
                border-radius: 12px;
                padding: 25px;
                font-size: 14px;
                font-weight: bold;
                min-height: 80px;
                min-width: 150px;
            }
            QPushButton.menu_btn:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6b46c1
                );
            }
            QPushButton.menu_btn:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4c51bf, stop:1 #553c9a
                );
            }
            QPushButton#btn_salir {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f56565, stop:1 #c53030
                );
                color: white;
                border: none;
                border-radius: 12px;
                padding: 25px;
                font-size: 14px;
                font-weight: bold;
                min-height: 80px;
                min-width: 150px;
            }
            QPushButton#btn_salir:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e53e3e, stop:1 #9b2c2c
                );
            }
            QFrame#footer {
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 10px;
                padding: 10px;
            }
            QLabel#footer_text {
                color: #718096;
                font-size: 12px;
            }
        """

    def crear_header(self):
        header = QFrame()
        header.setObjectName("header")
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel("🩺")
        icon_label.setStyleSheet("font-size: 48px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(icon_label)

        titulo = QLabel("Citas Médicas")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(titulo)

        subtitulo = QLabel("Solicite y gestione sus citas")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitulo)

        return header

    def crear_menu_botones(self):
        container = QFrame()
        container.setObjectName("menu_container")

        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        botones = [
            ("Agendar Cita", self.abrir_agendar_cita),
            ("Consultar Citas", self.consultar_citas),
            ("Modificar Cita", self.modificar_cita),
            ("Eliminar Cita", self.eliminar_cita),
        ]

        for i, (texto, handler) in enumerate(botones):
            btn = QPushButton(texto)
            btn.setProperty("class", "menu_btn")
            btn.clicked.connect(handler)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            row = i // 2
            col = i % 2
            grid_layout.addWidget(btn, row, col)

        btn_salir = QPushButton("🚪 Salir del\nMódulo")
        btn_salir.setObjectName("btn_salir")
        btn_salir.clicked.connect(self.close)
        btn_salir.setCursor(Qt.CursorShape.PointingHandCursor)
        grid_layout.addWidget(btn_salir, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        return container

    def crear_footer(self):
        footer = QFrame()
        footer.setObjectName("footer")
        footer_layout = QHBoxLayout(footer)

        footer_text = QLabel("© 2025 Sistema de Gestión Hospitalaria - Citas Médicas")
        footer_text.setObjectName("footer_text")
        footer_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(footer_text)

        return footer

    # --- Handlers ---
    def abrir_agendar_cita(self):
        ventana = AgendarCitaView(self.paciente_controller)
        ventana.setWindowTitle("Agendar Cita")
        ventana.show()
        self.ventanas_abiertas['agendar'] = ventana

    def consultar_citas(self):
        QMessageBox.information(self, "Consultar Citas", "Funcionalidad de consulta de citas en desarrollo.")

    def modificar_cita(self):
        QMessageBox.information(self, "Modificar Cita", "Funcionalidad de modificación en desarrollo.")

    def eliminar_cita(self):
        QMessageBox.information(self, "Eliminar Cita", "Funcionalidad de eliminación en desarrollo.")


def main():
    # Permite probar la vista de forma independiente
    app = None
    try:
        from PyQt6.QtWidgets import QApplication
        import sys
        app = QApplication(sys.argv)
    except Exception:
        pass

    # Si se ejecuta como script, creamos un controlador mínimo falso si hace falta
    try:
        from Citas_Medicas.controllers.paciente_controller import PacienteController
        from Citas_Medicas.models.agenda import Agenda
        agenda = Agenda()
        pc = PacienteController(agenda)
    except Exception:
        pc = None

    ventana = MenuPaciente(pc)
    ventana.show()

    if app:
        sys.exit(app.exec())


if __name__ == '__main__':
    main()

