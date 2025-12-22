import sys
from PyQt6.QtWidgets import QApplication

# Intentamos import absoluto (ejecución desde workspace root),
# si falla usamos imports relativos para ejecutar como script.
try:
    from Citas_Medicas.models.agenda import Agenda
    from Citas_Medicas.controllers.cita_controller import CitaController
    from Citas_Medicas.controllers.paciente_controller import PacienteController
    from Citas_Medicas.controllers.recepcionista_controller import RecepcionistaController
    from Citas_Medicas.controllers.jefe_controller import JefeController

    from Citas_Medicas.views.main_window import MainWindow
    from Citas_Medicas.views.menu_paciente import MenuPaciente
    from Citas_Medicas.views.menu_recepcionista import MenuRecepcionista
    from Citas_Medicas.views.menu_jefe import MenuJefe
except Exception:
    from models.agenda import Agenda
    from controllers.cita_controller import CitaController
    from controllers.paciente_controller import PacienteController
    from controllers.recepcionista_controller import RecepcionistaController
    from controllers.jefe_controller import JefeController

    from views.main_window import MainWindow
    from views.menu_paciente import MenuPaciente
    from views.menu_recepcionista import MenuRecepcionista
    from views.menu_jefe import MenuJefe


APP_STYLE = """
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


def main():
    app = QApplication(sys.argv)

    # --- MODELO Y CONTROLADORES ---
    agenda = Agenda()
    cita_controller = CitaController(agenda)

    paciente_controller = PacienteController(cita_controller)
    recepcionista_controller = RecepcionistaController(cita_controller)
    jefe_controller = JefeController(agenda)

    # --- VENTANA PRINCIPAL (Selector de Rol) ---
    main_window = MainWindow()
    main_window.setStyleSheet(APP_STYLE)

    # Conexión de botones a los menús (mantener referencia para evitar cierre)
    def abrir_menu_paciente():
        main_window.ventana_paciente = MenuPaciente(paciente_controller)
        main_window.ventana_paciente.show()

    def abrir_menu_recepcionista():
        main_window.ventana_recepcionista = MenuRecepcionista(recepcionista_controller)
        main_window.ventana_recepcionista.show()

    def abrir_menu_jefe():
        main_window.ventana_jefe = MenuJefe(jefe_controller)
        main_window.ventana_jefe.show()

    main_window.btn_paciente.clicked.connect(abrir_menu_paciente)
    main_window.btn_recepcionista.clicked.connect(abrir_menu_recepcionista)
    main_window.btn_jefe.clicked.connect(abrir_menu_jefe)

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
