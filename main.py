import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from Pacientes import PacienteView, PacienteController
from Consulta_Externa.consulta_controller import ConsultaExternaController
from Consulta_Externa.consulta_view import ConsultaExternaView
from Hospitalizacion.hospitalizacion_view import HospitalizacionView
from Farmacia.ventana_farmacia import VentanaFarmacia
from Citas_Medicas import CitasMedicasView, CitasMedicasController

from Medicos.medicos import VentanaPrincipal

class MenuPrincipal(QMainWindow):
    """
    Menú principal del sistema de gestión hospitalaria.
    Proporciona acceso a todos los módulos del sistema.
    """

    def __init__(self):
        super().__init__()
        self.ventanas_abiertas = {}
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de usuario del menú principal."""
        self.setWindowTitle("Sistema de Gestión Hospitalaria")
        self.setMinimumSize(900, 900)
        self.setStyleSheet(self.get_styles())

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 30, 40, 30)

        # Encabezado con logo e información
        header = self.crear_header()
        main_layout.addWidget(header)

        # Contenedor de botones del menú
        menu_container = self.crear_menu_botones()
        main_layout.addWidget(menu_container)

        # Footer
        footer = self.crear_footer()
        main_layout.addWidget(footer)

    def get_styles(self):
        """Retorna los estilos CSS para la aplicación."""
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
        """Crea el encabezado con título y descripción."""
        header = QFrame()
        header.setObjectName("header")
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icono/Logo
        icon_label = QLabel("🏥")
        icon_label.setStyleSheet("font-size: 48px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(icon_label)

        # Título
        titulo = QLabel("Sistema de Gestión Hospitalaria")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel("Seleccione un módulo para comenzar")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitulo)

        return header

    def crear_menu_botones(self):
        """Crea el contenedor con los botones del menú."""
        container = QFrame()
        container.setObjectName("menu_container")

        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        # Definir los módulos del menú
        modulos = [
            ("📅 Citas\nMédicas", self.abrir_citas_medicas),
            ("👤 Pacientes", self.abrir_pacientes),
            ("🩺 Consulta\nExterna", self.abrir_consulta_externa),
            ("💊 Farmacia", self.abrir_farmacia),
            ("🏨 Hospitalización", self.abrir_hospitalizacion),
            ("👨‍⚕️ Médicos", self.abrir_medicos),
        ]

        # Crear botones en una cuadrícula 2x3
        for i, (texto, funcion) in enumerate(modulos):
            btn = QPushButton(texto)
            btn.setProperty("class", "menu_btn")
            btn.clicked.connect(funcion)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            row = i // 3
            col = i % 3
            grid_layout.addWidget(btn, row, col)

        # Botón de salir (fila separada, centrado)
        btn_salir = QPushButton("🚪 Salir del\nSistema")
        btn_salir.setObjectName("btn_salir")
        btn_salir.clicked.connect(self.salir_sistema)
        btn_salir.setCursor(Qt.CursorShape.PointingHandCursor)
        grid_layout.addWidget(btn_salir, 2, 1)

        return container

    def crear_footer(self):
        """Crea el pie de página."""
        footer = QFrame()
        footer.setObjectName("footer")
        footer_layout = QHBoxLayout(footer)

        footer_text = QLabel("© 2025 Sistema de Gestión Hospitalaria - Todos los derechos reservados")
        footer_text.setObjectName("footer_text")
        footer_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(footer_text)

        return footer

    def abrir_citas_medicas(self):
        if "citas_medicas" not in self.ventanas_abiertas or not self.ventanas_abiertas["citas_medicas"].isVisible():
            controller = CitasMedicasController()
            ventana = CitasMedicasView(controller)
            ventana.setWindowTitle("Citas Médicas - Submódulo")
            self.ventanas_abiertas["citas_medicas"] = ventana
            ventana.show()
            ventana.raise_()
            ventana.activateWindow()

    def abrir_pacientes(self):
        """Abre el módulo de gestión de pacientes."""
        if "pacientes" not in self.ventanas_abiertas or not self.ventanas_abiertas["pacientes"].isVisible():
            controller = PacienteController()
            ventana = PacienteView(controller)
            ventana.setWindowTitle("Gestión de Pacientes - Submódulo")
            self.ventanas_abiertas["pacientes"] = ventana

        self.ventanas_abiertas["pacientes"].show()
        self.ventanas_abiertas["pacientes"].raise_()
        self.ventanas_abiertas["pacientes"].activateWindow()

    def abrir_consulta_externa(self):
        """Abre el módulo de consulta externa."""
        if "consulta_externa" not in self.ventanas_abiertas or not self.ventanas_abiertas["consulta_externa"].isVisible():
            controller = ConsultaExternaController()
            ventana = ConsultaExternaView(controller)
            ventana.setWindowTitle("Atención de Consultas Externas")
            ventana.resize(800, 700) # Tamaño cómodo para formularios
            self.ventanas_abiertas["consulta_externa"] = ventana
            self.ventanas_abiertas["hospitalizacion"] = ventana

        w = self.ventanas_abiertas["hospitalizacion"]
        w.show()
        try:
            w.showMaximized()
        except Exception:
            pass
        w.raise_()
        w.activateWindow()
        # Ocultar el menú principal mientras Hospitalización está abierta
        self.hide()

    def abrir_farmacia(self):
        """Abre el módulo de farmacia."""
        if "farmacia" not in self.ventanas_abiertas or not self.ventanas_abiertas["farmacia"].isVisible():
            ventana = VentanaFarmacia()
            ventana.setWindowTitle("Gestión de Farmacia - Submódulo")
            self.ventanas_abiertas["farmacia"] = ventana

        self.ventanas_abiertas["farmacia"].show()
        self.ventanas_abiertas["farmacia"].raise_()
        self.ventanas_abiertas["farmacia"].activateWindow()

    def abrir_hospitalizacion(self):
        """Abre el módulo de hospitalización."""
        if "hospitalizacion" not in self.ventanas_abiertas or not self.ventanas_abiertas["hospitalizacion"].isVisible():
            ventana = HospitalizacionView(parent=self)
            ventana.setWindowTitle("Gestión de Hospitalización - Submódulo")
            self.ventanas_abiertas["hospitalizacion"] = ventana

        w = self.ventanas_abiertas["hospitalizacion"]
        w.show()
        try:
            w.showMaximized()
        except Exception:
            pass
        w.raise_()
        w.activateWindow()
        # Ocultar el menú principal mientras Hospitalización está abierta
        self.hide()

    def abrir_medicos(self):
        """Abre el módulo de gestión de médicos."""
        # Verificar si la ventana ya está creada y visible para no abrirla dos veces
        if "medicos" not in self.ventanas_abiertas or not self.ventanas_abiertas["medicos"].isVisible():
            
            # Instanciar la clase que importamos. 
            # NOTA: Si tu clase requiere un controlador o argumentos, agrégalos aquí.
            ventana = VentanaPrincipal() 
            
            ventana.setWindowTitle("Gestión de Médicos")
            self.ventanas_abiertas["medicos"] = ventana

        # Mostrar la ventana y traerla al frente
        self.ventanas_abiertas["medicos"].show()
        self.ventanas_abiertas["medicos"].raise_()
        self.ventanas_abiertas["medicos"].activateWindow()

    def salir_sistema(self):
        """Confirma y cierra la aplicación."""
        respuesta = QMessageBox.question(
            self,
            "Confirmar Salida",
            "¿Está seguro de que desea salir del sistema?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            # Cerrar todas las ventanas abiertas
            for ventana in self.ventanas_abiertas.values():
                if ventana.isVisible():
                    ventana.close()
            self.close()

    def closeEvent(self, event):
        """Maneja el evento de cierre de la ventana."""
        # Cerrar todas las ventanas secundarias
        for ventana in self.ventanas_abiertas.values():
            if ventana.isVisible():
                ventana.close()
        event.accept()


def main():
    app = QApplication(sys.argv)

    # Configurar el estilo de la aplicación
    app.setStyle("Fusion")

    # Crear y mostrar el menú principal
    ventana = MenuPrincipal()
    ventana.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
