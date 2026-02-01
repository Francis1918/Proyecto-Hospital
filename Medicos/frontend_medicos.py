import sys
import os

# --- CORRECCIÓN DE RUTAS (IMPORTANTE) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
# ----------------------------------------

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QStackedWidget, QLabel
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QParallelAnimationGroup
from PyQt6.QtGui import QIcon

# Ahora estos imports funcionarán correctamente
import theme
from pages.registrar_page import WidgetRegistrar
from pages.consultar_page import WidgetConsultar

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Médico - Modularizado")
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
        
        # CORRECCIÓN 1: En lugar de setFixedWidth, fijamos min y max por separado
        # Esto permite que la animación pueda modificar ambos valores.
        self.sidebar.setMinimumWidth(220)
        self.sidebar.setMaximumWidth(220)
        
        layout_sidebar = QVBoxLayout(self.sidebar)
        layout_sidebar.setContentsMargins(0, 0, 0, 0)
        layout_sidebar.setSpacing(5)

        # Botón Menú
        self.btn_menu = QPushButton(" MENU")
        self.btn_menu.setIcon(QIcon(theme.asset_url("menu.svg")))
        self.btn_menu.setIconSize(QSize(24, 24))
        self.btn_menu.setFixedHeight(60)
        self.btn_menu.setStyleSheet("background: transparent; color: white; font-weight: bold; border: none; text-align: left; padding-left: 20px;")
        self.btn_menu.clicked.connect(self.toggle_sidebar)
        layout_sidebar.addWidget(self.btn_menu)

        # Navegación
        self.nav_btns = []
        items = [
            ("Registrar", "user_add.svg", 0),
            ("Consultar", "list.svg", 1)
        ]

        for texto, icono, idx in items:
            btn = QPushButton(f" {texto}")
            btn.setIcon(QIcon(theme.asset_url(icono)))
            btn.setIconSize(QSize(20, 20))
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(theme.STYLES["sidebar_btn"])
            
            btn.clicked.connect(lambda ch, i=idx: self.cambiar_pagina(i))
            self.nav_btns.append(btn)
            layout_sidebar.addWidget(btn)

        layout_sidebar.addStretch()
        
        # Footer
        lbl_ver = QLabel("v5.1")
        lbl_ver.setStyleSheet(f"color: {theme.Palette.Text_Light}; padding: 10px;")
        lbl_ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_sidebar.addWidget(lbl_ver)

        # --- Contenido ---
        self.stack = QStackedWidget()
        self.pag_registrar = WidgetRegistrar()
        self.pag_consultar = WidgetConsultar()
        
        self.stack.addWidget(self.pag_registrar)
        self.stack.addWidget(self.pag_consultar)

        # Conexión de señal
        self.pag_registrar.medico_guardado.connect(self.pag_consultar.cargar_datos)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)
        
        self.nav_btns[0].click()

    def cambiar_pagina(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_btns):
            btn.setChecked(i == idx)

    def toggle_sidebar(self):
        # CORRECCIÓN 2: Lógica de animación robusta
        ancho_actual = self.sidebar.width()
        
        if ancho_actual > 100:
            # Colapsar (220 -> 70)
            nuevo_ancho = 70
            self.btn_menu.setText("") 
            for btn in self.nav_btns:
                btn.setText("")
        else:
            # Expandir (70 -> 220)
            nuevo_ancho = 220
            self.btn_menu.setText(" MENU")
            # Restauramos textos
            textos = ["Registrar", "Consultar"]
            for i, btn in enumerate(self.nav_btns):
                btn.setText(f" {textos[i]}")

        # Usamos un GRUPO de animación para mover minWidth y maxWidth a la vez
        self.anim_group = QParallelAnimationGroup()
        
        anim_min = QPropertyAnimation(self.sidebar, b"minimumWidth")
        anim_min.setDuration(400)
        anim_min.setStartValue(ancho_actual)
        anim_min.setEndValue(nuevo_ancho)
        anim_min.setEasingCurve(QEasingCurve.Type.InOutQuart)

        anim_max = QPropertyAnimation(self.sidebar, b"maximumWidth")
        anim_max.setDuration(400)
        anim_max.setStartValue(ancho_actual)
        anim_max.setEndValue(nuevo_ancho)
        anim_max.setEasingCurve(QEasingCurve.Type.InOutQuart)

        self.anim_group.addAnimation(anim_min)
        self.anim_group.addAnimation(anim_max)
        self.anim_group.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())