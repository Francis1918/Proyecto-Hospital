"""
Widgets personalizados para el sistema hospitalario.
"""
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from core.theme import AppPalette
import core.utils as utils


class SidebarButton(QPushButton):
    """
    Botón personalizado para el sidebar con soporte de íconos
    y dos modos: expandido y colapsado.
    """
    
    def __init__(self, text, icon_name, page_index):
        super().__init__(text)
        self.page_index = page_index
        self.icon_name = icon_name
        self.is_collapsed = False
        self.is_active = False
        self.original_text = text  # Guardar el texto original
        
        # Configuración inicial
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(40)
        
        # Cargar ícono
        if icon_name:
            self.setIcon(utils.get_icon(icon_name, AppPalette.text_secondary))
        
        # Aplicar estilo inicial
        self.update_style(False)
    
    def update_style(self, is_active):
        """Actualiza el estilo del botón según si está activo o no"""
        self.is_active = is_active
        
        if is_active:
            bg_color = AppPalette.hover
            text_color = AppPalette.Primary
            icon_color = AppPalette.Primary
        else:
            bg_color = "transparent"
            text_color = AppPalette.text_primary
            icon_color = AppPalette.text_secondary
        
        # Actualizar ícono con color apropiado
        if self.icon_name:
            self.setIcon(utils.get_icon(self.icon_name, icon_color))
        
        if self.is_collapsed:
            # Modo colapsado: centrado, sin padding izquierdo
            self.setStyleSheet(f"""
                QPushButton {{
                    color: {text_color};
                    background-color: {bg_color};
                    text-align: center;
                    border: none;
                    border-radius: 8px;
                    font-weight: 500;
                    padding: 0px;
                }}
                QPushButton:hover {{
                    background-color: {AppPalette.hover};
                }}
            """)
        else:
            # Modo expandido: texto a la izquierda
            self.setStyleSheet(f"""
                QPushButton {{
                    color: {text_color};
                    background-color: {bg_color};
                    text-align: left;
                    padding-left: 15px;
                    border: none;
                    border-radius: 8px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {AppPalette.hover};
                }}
            """)
    
    def set_collapsed_mode(self, collapsed):
        """Cambia entre modo expandido y colapsado"""
        self.is_collapsed = collapsed
        if collapsed:
            self.setText("")  # Ocultar texto en modo colapsado
        else:
            self.setText(self.original_text)  # Restaurar texto original
        # Reaplica el estilo con el estado activo actual
        self.update_style(self.is_active)

