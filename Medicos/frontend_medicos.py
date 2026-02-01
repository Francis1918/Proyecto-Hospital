import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QStackedWidget, QLabel
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QParallelAnimationGroup
from PyQt6.QtGui import QIcon

import theme
import utils # Importamos utils para colorear iconos
from pages.registrar_page import WidgetRegistrar
from pages.consultar_page import WidgetConsultar

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Médico")
        self.resize(1100, 750)
        self.setStyleSheet(theme.get_sheet())

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setMinimumWidth(180) # Un poco más ancho para el estilo moderno
        self.sidebar.setMaximumWidth(180)
        
        layout_sidebar = QVBoxLayout(self.sidebar)
        layout_sidebar.setContentsMargins(0, 10, 0, 20) # Margen arriba y abajo
        layout_sidebar.setSpacing(10)

        # --- HEADER DEL SIDEBAR ---
        self.header_sidebar = QFrame()
        self.header_sidebar.setStyleSheet("background: transparent;")
        layout_header = QHBoxLayout(self.header_sidebar)
        layout_header.setContentsMargins(0, 10, 0, 10)
    
        self.lbl_app_name = QLabel("Medicos")
        self.lbl_app_name.setObjectName("h2")
        
        # Botón para colapsar (ahora es pequeño y a la derecha)
        self.btn_menu = QPushButton()
        self.btn_menu.setIcon(utils.get_icon("menu.svg", color=theme.Palette.Bg_Main)) 
        self.btn_menu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_menu.setFixedSize(32, 32)
        self.btn_menu.setStyleSheet("border: none; border-radius: 20px;")
        self.btn_menu.clicked.connect(self.toggle_sidebar)

        layout_header.addStretch()    
        layout_header.addWidget(self.lbl_app_name)
        layout_header.addWidget(self.btn_menu)
        layout_header.addStretch()
        
        layout_sidebar.addWidget(self.header_sidebar)

        # --- Separador Sutil ---
        cont_line = QHBoxLayout()
        cont_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_sidebar.addLayout(cont_line)
        
        layout_sidebar.addSpacing(6)

        # --- Navegación ---
        self.nav_btns = []
        items = [
            ("Registrar", "user_add.svg", 0),
            ("Consultar", "list.svg", 1)
        ]

        for texto, icono, idx in items:
            btn = QPushButton(f"{texto}")
            btn.setIcon(utils.get_icon(icono, color=theme.Palette.Bg_Main))
            btn.setIconSize(QSize(20, 20))
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(theme.STYLES["sidebar_btn"])
            
            btn.clicked.connect(lambda ch, i=idx: self.cambiar_pagina(i))
            self.nav_btns.append(btn)
            layout_sidebar.addWidget(btn)

        layout_sidebar.addStretch()


        # --- Contenido ---
        self.stack = QStackedWidget()
        self.pag_registrar = WidgetRegistrar()
        self.pag_consultar = WidgetConsultar()
        
        self.stack.addWidget(self.pag_registrar)
        self.stack.addWidget(self.pag_consultar)

        self.pag_registrar.medico_guardado.connect(self.pag_consultar.cargar_datos)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)
        
        self.nav_btns[0].click()

    def cambiar_pagina(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_btns):
            btn.setChecked(i == idx)
            color_icon = theme.Palette.Text_Primary if i == idx else theme.Palette.Bg_Main
            icon_name = "user_add.svg" if i == 0 else "list.svg" 
            btn.setIcon(utils.get_icon(icon_name, color=color_icon))


    def toggle_sidebar(self):
        ancho_actual = self.sidebar.width()
        
        if ancho_actual > 100:
            # Colapsar
            nuevo_ancho = 70
            self.lbl_app_name.hide()
            for btn in self.nav_btns:
                btn.setText("")
        else:
            # Expandir
            nuevo_ancho = 180
            self.lbl_app_name.show()
            textos = ["Registrar", "Consultar"]
            for i, btn in enumerate(self.nav_btns):
                btn.setText(f"  {textos[i]}")

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
        self.anim_group.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())