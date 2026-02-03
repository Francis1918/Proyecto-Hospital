import sys
import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt

from core.utils import get_icon

# Configuración de ruta para core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.theme import AppPalette as HospitalPalette, get_sheet
from Hospitalizacion.evolucion_cuidados.evolucion_cuidados_view import EvolucionCuidadosView
from Hospitalizacion.camas_y_salas.camas_salas_view import CamasSalasView
from Hospitalizacion.Visitas.visitas_view import VisitasView
# Importar la gestión de órdenes que ya existe en tu repo
from Hospitalizacion.gestion_orden.orden_view import GestionOrdenView

class HospitalizacionView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.padre = parent
        self.init_ui()

    def init_ui(self):
        # Aplicar el stylesheet global para asegurar colores legibles en inputs
        try:
            self.setStyleSheet(get_sheet())
        except Exception:
            # Fallback a fondo simple si falla
            self.setStyleSheet(f"background-color: {HospitalPalette.bg_main};")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- ENCABEZADO (Header idéntico a Pacientes) ---
        self.header_frame = QFrame()
        self.header_frame.setStyleSheet("background-color: white;")
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # 1. Cambiamos QWidget por QFrame para poder darle estilo
        titulo_container = QFrame()
        
        # 2. Aplicamos el estilo: Fondo blanco, borde gris suave y esquinas redondeadas
        titulo_container.setStyleSheet(f"""
            QFrame {{
                background-color: {HospitalPalette.white_02}; 
                border-radius: 8px;
            }}
        """)

        # 3. Configuramos el layout interno
        titulo_layout = QHBoxLayout(titulo_container)
        titulo_layout.setContentsMargins(20, 15, 20, 15)

        # --- CONTENIDO (Icono + Texto) ---
        # Icono
        icon_lbl = QLabel()
        icon_pixmap = get_icon("building-hospital.svg", color=HospitalPalette.Primary, size=40).pixmap(40, 40)
        icon_lbl.setPixmap(icon_pixmap)
        
        # Textos
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        self.lbl_titulo = QLabel("Hospitalización")
        self.lbl_titulo.setObjectName("h1")
        
        lbl_sub = QLabel("Gestión de camas, evolución clínica, órdenes y visitas.")
        lbl_sub.setStyleSheet(f"color: {HospitalPalette.black_02}; font-size: 14px;")
        
        text_layout.addWidget(self.lbl_titulo)
        text_layout.addWidget(lbl_sub)

        # Añadimos al layout horizontal del contenedor
        titulo_layout.addWidget(icon_lbl)
        titulo_layout.addSpacing(15)
        titulo_layout.addLayout(text_layout)
        titulo_layout.addStretch()

        # Finalmente lo agregamos al header principal
        header_layout.addWidget(titulo_container)

        # --- BARRA DE PESTAÑAS (Sin "Inicio") ---
        self.nav_bar = QWidget()
        self.nav_bar.setFixedHeight(50)
        nav_layout = QHBoxLayout(self.nav_bar)
        nav_layout.setContentsMargins(10, 0, 10, 0)
        nav_layout.setSpacing(8)

        self.btns = []
        # Solo módulos con contenido
        self.tabs_info = [
            ("Camas y Salas", 0),
            ("Evolución y Cuidados", 1),
            ("Órdenes Médicas", 2),
            ("Visitas", 3),
            ("Admisión y Alta", 4)
        ]

        for texto, index in self.tabs_info:
            btn = self.crear_nav_btn(texto, index)
            self.btns.append(btn)
            nav_layout.addWidget(btn)
        
        nav_layout.addStretch()
        header_layout.addWidget(self.nav_bar)
        self.main_layout.addWidget(self.header_frame)

        # --- CONTENEDOR DE VISTAS (STACK) ---
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # Inyectamos las vistas reales que están en el repositorio
        self.stack.addWidget(CamasSalasView("Admin"))               # Index 0
        self.stack.addWidget(EvolucionCuidadosView(self))           # Index 1
        self.stack.addWidget(GestionOrdenView("Admin"))             # Index 2
        self.stack.addWidget(VisitasView(self))                     # Index 3
        self.stack.addWidget(self.crear_placeholder("Admisión"))    # Index 4

        self.cambiar_pestana(0) # Inicia directamente en Camas

    def crear_nav_btn(self, texto, index):
        btn = QPushButton(texto)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(45)
        btn.clicked.connect(lambda: self.cambiar_pestana(index))
        return btn

    def cambiar_pestana(self, index):
        self.stack.setCurrentIndex(index)
        estilo_base = f"padding: 0 15px; border: none; font-weight: bold; font-size: 13px; color: {HospitalPalette.black_02}; background: transparent;"
        estilo_activo = f"color: {HospitalPalette.Primary}; border-bottom: 3px solid {HospitalPalette.Primary};"
        
        for i, btn in enumerate(self.btns):
            btn.setStyleSheet(estilo_base + (estilo_activo if i == index else ""))

    def regresar_al_menu(self):
        self.cambiar_pestana(0)

    def crear_placeholder(self, nombre):
        view = QWidget()
        layout = QVBoxLayout(view)
        lbl = QLabel(f"El módulo de {nombre} requiere integración de base de datos.")
        lbl.setStyleSheet(f"color: {HospitalPalette.black_02};")
        layout.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        return view

    def closeEvent(self, event):
        if self.padre: self.padre.show()
        event.accept()