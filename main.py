import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QStackedWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup

# --- IMPORTACIONES ---
import core.utils as utils
from core.theme import AppPalette as HospitalPalette
from core.widgets import SidebarButton

# Importamos tus módulos (Asegúrate de que las carpetas existan)
from Pacientes.paciente_view import PacienteView
from Pacientes.paciente_controller import PacienteController
from Consulta_Externa.consulta_controller import ConsultaExternaController
from Consulta_Externa.consulta_view import ConsultaExternaView
from Hospitalizacion.hospitalizacion_view import HospitalizacionView
from Farmacia.frontend.frontend_farmacia import VentanaFarmacia
from Citas_Medicas import CitasMedicasView, CitasMedicasController
from core.database import inicializar_db
from Medicos.frontend import module_medicos

class MenuPrincipal(QMainWindow):
    """
    Menú principal del sistema de gestión hospitalaria.
    Proporciona acceso a todos los módulos del sistema.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Hospitalario")
        self.resize(1200, 800)
        self.setStyleSheet(f"background-color: {HospitalPalette.bg_main};")

        self.sidebar_expanded = True
        self.nav_btns = []
        self.section_labels = []

        # Widget Central y Layout Principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout Horizontal: Sidebar | Contenido
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Crear Sidebar
        self.setup_sidebar()
        # 2. Crear Stack de Contenido
        self.setup_content()
        # 3. Cargar Módulos
        self.load_modules()

    def setup_sidebar(self):
        """Configura el panel lateral estilo Folderly con Tarjetas"""
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(240)
        # Fondo del sidebar un poco más gris para que resalten las tarjetas blancas
        self.sidebar.setStyleSheet(f"""
            QFrame#Sidebar {{
                background-color: {HospitalPalette.bg_sidebar}; 
                border-right: 1px solid #e5e7eb;
            }}
        """)
        
        layout = QVBoxLayout(self.sidebar)
        # Márgenes externos (espacio entre el borde de la ventana y las tarjetas)
        layout.setContentsMargins(8, 8, 8, 8) 
        layout.setSpacing(10)

        # --- HEADER (Tarjeta 1) ---
        self.header_widget = QWidget()
        self.header_widget.setStyleSheet("background: #FFFFFF; border: none; border-radius: 8px;")
        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(15, 8, 15, 8)
        
        self.lbl_logo = QLabel("Hospital\nManager")
        self.lbl_logo.setStyleSheet(f"color: {HospitalPalette.text_primary}; font-weight: bold; font-size: 15px;")
        
        self.icon_app = QLabel()
        self.icon_app.setPixmap(utils.get_icon("activity.svg", HospitalPalette.Primary, 26).pixmap(26, 26))
        
        self.btn_toggle = QPushButton()
        self.btn_toggle.setIcon(utils.get_icon("menu.svg", HospitalPalette.text_secondary))
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setFixedSize(30, 30)
        self.btn_toggle.setStyleSheet("background: transparent; border: none;")
        self.btn_toggle.clicked.connect(self.toggle_sidebar)
        
        self.header_layout.addWidget(self.icon_app)
        self.header_layout.addWidget(self.lbl_logo)
        self.header_spacer = QWidget()
        self.header_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.header_layout.addWidget(self.header_spacer)
        self.header_layout.addWidget(self.btn_toggle)

        layout.addWidget(self.header_widget)
        
        # Tarjeta 1: GENERAL
        self.crear_seccion_menu(layout, "GENERAL", [
            ("Inicio", "activity.svg", 0),
            ("Citas Médicas", "calendar.svg", 1),
            ("Pacientes", "users.svg", 2)
        ])

        # Tarjeta 2: CLÍNICA
        self.crear_seccion_menu(layout, "CLÍNICA", [
            ("Consulta Externa", "clipboard.svg", 3),
            ("Hospitalización", "home.svg", 5),
            ("Médicos", "user-doctor.svg", 6)
        ])

        # Tarjeta 3: ADMINISTRACIÓN
        self.crear_seccion_menu(layout, "ADMINISTRACIÓN", [
            ("Farmacia", "pill.svg", 4)
        ])

        layout.addStretch()
        
        # Footer (Este lo dejamos fuera de tarjeta, o puedes meterlo en una si quieres)
        self.btn_salir = SidebarButton("Cerrar Sesión", "log-out.svg", -1)
        self.btn_salir.clicked.connect(self.close)
        self.btn_salir.setStyleSheet(f"""
            QPushButton {{
                color: #ef4444; background: transparent; text-align: left; padding-left: 15px; border: none; font-weight: 500; margin: 0 10px;
            }}
            QPushButton:hover {{ background-color: #fef2f2; border-radius: 8px; }}
        """)
        layout.addWidget(self.btn_salir)
        
        self.main_layout.addWidget(self.sidebar)

    def crear_seccion_menu(self, parent_layout, titulo, items):
        """
        Crea un panel redondeado (tarjeta) que contiene el título y los botones.
        """
        # 1. Crear el marco (Card)
        card_frame = QFrame()
        card_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 8px;
                border: none;
            }
        """)
        
        # 2. Layout interno de la tarjeta
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(8, 8, 8, 8)
        card_layout.setSpacing(4)

        # 3. Agregar Título
        lbl = QLabel(titulo)
        # margin-left para alinearlo con el texto de los botones
        lbl.setStyleSheet(f"background: transparent; color: {HospitalPalette.text_secondary}; font-size: 11px; font-weight: 700; margin-left: 12px; margin-bottom: 5px;")
        card_layout.addWidget(lbl)
        self.section_labels.append(lbl)

        # 4. Agregar Botones
        for texto, icono, indice in items:
            btn = SidebarButton(texto, icono, indice)
            btn.clicked.connect(lambda ch, b=btn: self.navegar(b))
            card_layout.addWidget(btn)
            self.nav_btns.append(btn)

        # 5. Añadir la tarjeta completa al sidebar
        parent_layout.addWidget(card_frame)

    def add_section_label(self, layout, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(f"background: transparent; color: {HospitalPalette.text_secondary}; font-size: 11px; font-weight: 700; margin-left: 20px; margin-top: 5px;")
        layout.addWidget(lbl)
        self.section_labels.append(lbl)

    def add_nav_btn(self, layout, text, icon, index):
        btn = SidebarButton(text, icon, index)
        btn.clicked.connect(lambda: self.navegar(btn))
        layout.addWidget(btn)
        self.nav_btns.append(btn)

    def setup_content(self):
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #ffffff;")
        self.main_layout.addWidget(self.stack)

    def navegar(self, sender_btn):
        # 1. Cambiar visualmente el activo
        for btn in self.nav_btns:
            btn.update_style(btn == sender_btn)
        # 2. Cambiar página del stack
        self.stack.setCurrentIndex(sender_btn.page_index)

    def toggle_sidebar(self):
        ancho_actual = self.sidebar.width()
        width_collapsed = 70  # Ancho colapsado
        width_expanded = 240  # Ancho expandido
        
        if self.sidebar_expanded:
            # --- COLAPSAR ---
            nuevo_ancho = width_collapsed        

            self.lbl_logo.hide()
            self.icon_app.hide()
            self.header_spacer.hide()

            for lbl in self.section_labels: lbl.hide()
            for btn in self.nav_btns: btn.set_collapsed_mode(True)
            self.btn_salir.set_collapsed_mode(True)

            # Ajustar márgenes del header al colapsar
            self.header_layout.setContentsMargins(0, 0, 0, 0)
            self.header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        else:
            # --- EXPANDIR ---
            nuevo_ancho = width_expanded
            # Restaurar márgenes originales del header
            self.header_layout.setContentsMargins(20, 0, 15, 0)
            self.header_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # Animación
        self.anim_group = QParallelAnimationGroup()
        
        anim_min = QPropertyAnimation(self.sidebar, b"minimumWidth")
        anim_min.setDuration(300)
        anim_min.setStartValue(ancho_actual)
        anim_min.setEndValue(nuevo_ancho)
        anim_min.setEasingCurve(QEasingCurve.Type.InOutQuad)

        anim_max = QPropertyAnimation(self.sidebar, b"maximumWidth")
        anim_max.setDuration(300)
        anim_max.setStartValue(ancho_actual)
        anim_max.setEndValue(nuevo_ancho)
        anim_max.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.anim_group.addAnimation(anim_min)
        self.anim_group.addAnimation(anim_max)
        
        # Conectar señal para restaurar textos AL FINAL de la expansión
        if not self.sidebar_expanded:
            self.anim_group.finished.connect(self.show_sidebar_text)
            
        self.anim_group.start()
        self.sidebar_expanded = not self.sidebar_expanded

    def show_sidebar_text(self):
        """Restaura los elementos visibles"""
        self.lbl_logo.show()
        self.icon_app.show()
        self.header_spacer.show()
        for lbl in self.section_labels: lbl.show()
        for btn in self.nav_btns: btn.set_collapsed_mode(False)
        self.btn_salir.set_collapsed_mode(False)
        
        # Restaurar estilo salir
        self.btn_salir.setStyleSheet(f"""
            QPushButton {{
                color: #ef4444; background: transparent; text-align: left; padding-left: 15px; border: none; font-weight: 500; margin: 0 10px;
            }}
            QPushButton:hover {{ background-color: #fef2f2; border-radius: 8px; }}
        """)

    def load_modules(self):
        # --- 0. Inicio (Dashboard) ---
        page_home = QWidget()
        l = QVBoxLayout(page_home)
        l.addWidget(QLabel("Dashboard Principal", alignment=Qt.AlignmentFlag.AlignCenter))
        self.stack.addWidget(page_home)

        # --- Helper para cargar ventanas QMainWindow dentro de widgets ---
        def embed(window):
            window.setWindowFlags(Qt.WindowType.Widget)
            window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
            window.show()
            return window

        # --- 1. Citas ---
        self.view_citas = embed(CitasMedicasView(controller=CitasMedicasController()))
        self.stack.addWidget(self.view_citas)

        # --- 2. Pacientes ---
        self.view_pacientes = embed(PacienteView(controller=PacienteController()))
        self.stack.addWidget(self.view_pacientes)

        # --- 3. Consulta (Ya es Widget) ---
        self.view_consulta = ConsultaExternaView(controller=ConsultaExternaController())
        self.stack.addWidget(self.view_consulta)

        # --- 4. Farmacia ---
        self.view_farmacia = embed(VentanaFarmacia())
        self.stack.addWidget(self.view_farmacia)

        # --- 5. Hospitalización ---
        self.view_hosp = embed(HospitalizacionView(parent=self))
        self.stack.addWidget(self.view_hosp)

        # --- 6. Médicos ---
        self.view_medicos = embed(module_medicos.VentanaPrincipal())
        self.stack.addWidget(self.view_medicos)

        # Iniciar en la primera opción
        if self.nav_btns:
            self.nav_btns[0].click()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MenuPrincipal()
    window.show()
    sys.exit(app.exec())