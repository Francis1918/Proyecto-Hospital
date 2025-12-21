import sys
from PyQt6.QtWidgets import QApplication
from Pacientes import PacienteView, PacienteController


def main():
    app = QApplication(sys.argv)

    # Inicializar el controlador con la conexión a la base de datos
    # db_connection = tu_conexion_a_base_de_datos()
    controller = PacienteController()

    # Crear y mostrar la vista
    ventana = PacienteView(controller)
    ventana.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()