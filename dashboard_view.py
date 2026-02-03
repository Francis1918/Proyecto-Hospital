# dashboard_view.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QToolButton, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont 
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from core.theme import AppPalette
from core.utils import get_icon

class DashboardView(QWidget):
    # Señal para pedir navegación: envía el índice de la página a la que ir
    solicitar_navegacion = pyqtSignal(int) 

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # --- 1. SALUDO E ILUSTRACIÓN ---
        top_section = QHBoxLayout()
        
        # Texto de Bienvenida
        text_layout = QVBoxLayout()
        lbl_saludo = QLabel("¡Bienvenido al Sistema!")
        lbl_saludo.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {AppPalette.text_primary};")
        
        lbl_sub = QLabel("Gestión Hospitalaria Integral v1.0")
        lbl_sub.setStyleSheet(f"font-size: 16px; color: {AppPalette.text_secondary};")
        
        text_layout.addWidget(lbl_saludo)
        text_layout.addWidget(lbl_sub)
        text_layout.addStretch()
        
        # Ilustración (SVG)
        lbl_img = QLabel()
        lbl_img.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Usamos get_icon sin color para mantener los colores originales del SVG
        try:
            pixmap = get_icon("ilustracion-hospital.svg", size=250).pixmap(300, 250)
            lbl_img.setPixmap(pixmap)
        except:
            pass # Si no existe la imagen, no falla

        top_section.addLayout(text_layout)
        top_section.addStretch()
        top_section.addWidget(lbl_img)
        
        layout.addLayout(top_section)

        # --- 2. SECCIÓN DE ATAJOS (GRID) ---
        lbl_atajos = QLabel("Accesos Rápidos")
        lbl_atajos.setObjectName("h2")
        layout.addWidget(lbl_atajos)

        grid = QGridLayout()
        grid.setSpacing(20)

        # Definimos los atajos: (Título, Icono, Color de Fondo, Índice de Página)
        atajos = [
            ("Nueva Cita", "calendar.svg", AppPalette.Primary, 1),
            ("Registrar Paciente", "user-plus.svg", AppPalette.Success, 2),
            ("Consulta Externa", "clipboard.svg", "#805AD5", 3), # Morado
            ("Ver Médicos", "user-doctor.svg", "#DD6B20", 5),    # Naranja
        ]

        for i, (texto, icono, color, index) in enumerate(atajos):
            btn = self.crear_tarjeta_atajo(texto, icono, color, index)
            grid.addWidget(btn, 0, i) # Todos en la fila 0

        layout.addLayout(grid)
        layout.addStretch()

    def crear_tarjeta_atajo(self, texto, icono, color_base, index):
        """Crea un botón grande estilo tarjeta usando QToolButton."""
        btn = QToolButton()
        btn.setText(texto)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(200, 130)
        
        # --- FIX PARA EL ERROR "Point size <= 0" ---
        # Definimos la fuente en Python para asegurar que tenga un tamaño base válido
        btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        # -------------------------------------------

        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btn.setIcon(get_icon(icono, color=color_base, size=48))
        btn.setIconSize(QSize(48, 48))
        
        # El estilo CSS se mantiene igual
        btn.setStyleSheet(f"""
            QToolButton {{
                background-color: white;
                border: 1px solid {AppPalette.Border};
                border-radius: 12px;
                color: {AppPalette.text_primary};
                padding: 15px;
            }}
            QToolButton:hover {{
                background-color: {AppPalette.hover};
                border: 1px solid {color_base};
                color: {color_base};
            }}
            QToolButton:pressed {{
                background-color: {AppPalette.Focus_Bg};
            }}
        """)
        
        btn.clicked.connect(lambda: self.solicitar_navegacion.emit(index))
        
        return btn