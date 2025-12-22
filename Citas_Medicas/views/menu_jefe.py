from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt

try:
    from Citas_Medicas.controllers.jefe_controller import JefeController
    from Citas_Medicas.views.agenda.consultar_agenda_view import ConsultarAgendaView
except Exception:
    from controllers.jefe_controller import JefeController
    from views.agenda.consultar_agenda_view import ConsultarAgendaView


class MenuJefe(QMainWindow):
    def __init__(self, controller: JefeController):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Menú Jefe")
        self.setFixedSize(450, 300)

        central = QWidget()
        layout = QVBoxLayout()

        titulo = QLabel("Administración de Agenda")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size:18px; font-weight:bold;")

        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)

        btn_registrar = QPushButton("Registrar Agenda")
        btn_consultar = QPushButton("Consultar Agenda")

        btn_registrar.clicked.connect(self.registrar_agenda)
        btn_consultar.clicked.connect(self.consultar_agenda)

        layout.addWidget(titulo)
        layout.addWidget(linea)
        layout.addWidget(btn_registrar)
        layout.addWidget(btn_consultar)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def registrar_agenda(self):
        mensaje = self.controller.registrar_agenda()
        QMessageBox.information(self, "Agenda", mensaje)

    def consultar_agenda(self):
        self.ventana = ConsultarAgendaView(self.controller)
        self.ventana.show()
