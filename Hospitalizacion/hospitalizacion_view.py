import sys
import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt

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
        self.header_frame.setStyleSheet("background-color: white; border-bottom: 1px solid #e2e8f0;")
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        titulo_container = QWidget()
        titulo_layout = QHBoxLayout(titulo_container)
        self.lbl_titulo = QLabel("Hospitalización")
        self.lbl_titulo.setStyleSheet(f"color: {HospitalPalette.text_primary}; font-size: 26px; font-weight: bold; padding: 15px 20px;")
        titulo_layout.addWidget(self.lbl_titulo)
        titulo_layout.addStretch()
        header_layout.addWidget(titulo_container)

        # --- BARRA DE PESTAÑAS (Sin "Inicio") ---
        self.nav_bar = QWidget()
        self.nav_bar.setFixedHeight(50)
        nav_layout = QHBoxLayout(self.nav_bar)
        nav_layout.setContentsMargins(20, 0, 20, 0)
        nav_layout.setSpacing(10)

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
        self.stack.addWidget(CamasSalasView("Admin"))            # Index 0
        self.stack.addWidget(EvolucionCuidadosView(self))        # Index 1
        self.stack.addWidget(GestionOrdenView("Admin"))         # Index 2
        self.stack.addWidget(VisitasView(self))                  # Index 3
        self.stack.addWidget(self.crear_placeholder("Admisión")) # Index 4 (Aún no tiene vista funcional en el repo)

        self.cambiar_pestana(0) # Inicia directamente en Camas

    def crear_nav_btn(self, texto, index):
        btn = QPushButton(texto)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(45)
        btn.clicked.connect(lambda: self.cambiar_pestana(index))
        return btn

    def cambiar_pestana(self, index):
        self.stack.setCurrentIndex(index)
        estilo_base = f"padding: 0 15px; border: none; font-weight: bold; font-size: 13px; color: {HospitalPalette.text_secondary}; background: transparent;"
        estilo_activo = f"color: {HospitalPalette.Primary}; border-bottom: 3px solid {HospitalPalette.Primary};"
        
        for i, btn in enumerate(self.btns):
            btn.setStyleSheet(estilo_base + (estilo_activo if i == index else ""))

    def regresar_al_menu(self):
        self.cambiar_pestana(0)

    def crear_placeholder(self, nombre):
        view = QWidget()
        layout = QVBoxLayout(view)
        lbl = QLabel(f"El módulo de {nombre} requiere integración de base de datos.")
        lbl.setStyleSheet(f"color: {HospitalPalette.text_secondary};")
        layout.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        return view

    def closeEvent(self, event):
        if self.padre: self.padre.show()
        event.accept()