# pacientes/paciente_view.py

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QTabWidget, QFrame
)
from PyQt6.QtCore import Qt, QSize

# --- IMPORTACIONES DEL CORE ---
from Pacientes.views.consultar_view import ConsultarPacienteView
from Pacientes.views.registrar_view import RegistrarPacienteView
from core.theme import AppPalette, get_sheet, STYLES
from core.utils import get_icon
from .paciente_controller import PacienteController

class PacienteView(QMainWindow):
    def __init__(self, controller: PacienteController = None):
        super().__init__()
        self.controller = controller or PacienteController()
        self.init_ui()

    def init_ui(self):
        # 1. Configuración base y Tema
        self.setWindowTitle("Gestión de Pacientes")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(get_sheet())

        # 2. Widget Central
        central = QWidget()
        self.setCentralWidget(central)
        
        # Layout principal (Vertical)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- HEADER (Encabezado) ---
        header_frame = QFrame()
        # Fondo blanco suave para el header
        header_frame.setStyleSheet(f"background-color: {AppPalette.bg_sidebar}; border-radius: 8px;") 
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)

        # Icono grande
        icon_lbl = QLabel()
        icon_pixmap = get_icon("users.svg", color=AppPalette.Primary, size=40).pixmap(40, 40)
        icon_lbl.setPixmap(icon_pixmap)
        
        # Título y Subtítulo
        title_layout = QVBoxLayout()
        lbl_titulo = QLabel("Módulo de Pacientes")
        lbl_titulo.setObjectName("h1") # Usa el estilo definido en theme.py
        
        lbl_subtitulo = QLabel("Gestión de historias clínicas, datos personales y contacto.")
        lbl_subtitulo.setStyleSheet(f"color: {AppPalette.text_secondary}; font-size: 14px;")
        
        title_layout.addWidget(lbl_titulo)
        title_layout.addWidget(lbl_subtitulo)

        header_layout.addWidget(icon_lbl)
        header_layout.addSpacing(15)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        main_layout.addWidget(header_frame)

        # --- SISTEMA DE PESTAÑAS (TABS) ---
        self.tabs = QTabWidget()
        self.tabs.setIconSize(QSize(20, 20))
        
        # PESTAÑA 1: REGISTRAR 
        # Instanciamos la vista real (Ella sola se construye)
        self.tab_registrar = RegistrarPacienteView(self.controller)
        
        # PESTAÑA 2: CONSULTAR
        self.tab_consultar = ConsultarPacienteView(self.controller)
        # Agregamos las pestañas al widget
        self.tabs.addTab(
            self.tab_registrar, 
            get_icon("user-plus.svg", AppPalette.text_secondary), 
            "Registrar Nuevo"
        )
        
        self.tabs.addTab(
            self.tab_consultar, 
            get_icon("list.svg", AppPalette.text_secondary), 
            "Directorio de Pacientes"
        )

        # CONEXIONES DE SEÑALES (LOGICA)
        # 1. Cuando se guarde un paciente, recargar la tabla de consultas
        self.tab_registrar.paciente_registrado_signal.connect(self.tab_consultar.cargar_pacientes)       
        # 2. (Opcional) Cambiar automáticamente a la pestaña de "Directorio" al guardar
        self.tab_registrar.paciente_registrado_signal.connect(lambda: self.tabs.setCurrentIndex(1))
        main_layout.addWidget(self.tabs)
