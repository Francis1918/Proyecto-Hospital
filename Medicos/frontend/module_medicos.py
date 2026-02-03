# Medicos/frontend/frontend_medicos.py

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget
)
from PyQt6.QtCore import QSize

import core.theme as theme
import core.utils as utils 
from pages.registrar_page import WidgetRegistrar
from pages.consultar_page import WidgetConsultar

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Médico - Gestión Hospitalaria")
        self.resize(1100, 750)
        # Aplicamos el tema actualizado
        self.setStyleSheet(theme.get_sheet())

        # Widget Central
        central = QWidget()
        self.setCentralWidget(central)
        
        # Layout Principal (Vertical)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(15, 15, 15, 15) # Un poco de margen alrededor

        # --- CREACIÓN DEL SISTEMA DE TABS ---
        self.tabs = QTabWidget()
        self.tabs.setIconSize(QSize(20, 20))
        
        # Instanciamos las páginas
        self.pag_registrar = WidgetRegistrar()
        self.pag_consultar = WidgetConsultar()
        
        icon_add = utils.get_icon("user-add.svg", color=theme.AppPalette.Focus)
        icon_list = utils.get_icon("list.svg", color=theme.AppPalette.Focus)

        self.tabs.addTab(self.pag_registrar, icon_add, "Registrar Médico")
        self.tabs.addTab(self.pag_consultar, icon_list, "Consultar Base de Datos")

        # --- CONEXIÓN DE SEÑALES ---
        self.pag_registrar.medico_guardado.connect(self.al_guardar_medico)
        layout.addWidget(self.tabs)

    def al_guardar_medico(self):
        """
        Se ejecuta cuando WidgetRegistrar emite la señal 'medico_guardado'
        """
        # 1. Recargar la tabla de la pestaña consultar
        self.pag_consultar.cargar_datos()
        # 2. Cambiar a la pestaña consultar
        self.tabs.setCurrentIndex(1)