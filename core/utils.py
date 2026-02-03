# core/utils.py

import sys
import os
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt

# ==========================================
# 1. GESTIÓN DE RUTAS (Path System)
# ==========================================
def get_base_path():
    """Determina la ruta raíz del proyecto (funciona en DEV y en EXE compilado)."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        # core/utils.py -> subimos un nivel para llegar a la raíz del proyecto
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Definimos rutas globales
BASE_DIR = get_base_path()
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def asset_url(filename: str) -> str:
    """
    Devuelve la ruta absoluta string para usar en CSS (QSS).
    Ejemplo: url(C:/Proyecto/assets/icono.svg)
    """
    # Normalizamos slashes para que CSS de Qt lo entienda siempre
    path = os.path.join(ASSETS_DIR, filename).replace("\\", "/")
    return path

# ==========================================
# 2. GENERADOR DE ICONOS
# ==========================================
def get_icon(filename: str, color: str = None, size: int = 24) -> QIcon:
    """
    Busca un icono en la carpeta assets y lo colorea dinámicamente.
    """
    path = os.path.join(ASSETS_DIR, filename)

    if not os.path.exists(path):
        # Intenta buscar dentro de una subcarpeta 'icons' si no está en la raíz de assets
        path = os.path.join(ASSETS_DIR, "icons", filename)
        if not os.path.exists(path):
            print(f"⚠️ Icono no encontrado: {filename}")
            return QIcon()

    base_icon = QIcon(path)
    
    if not color:
        return base_icon

    # Renderizar a Pixmap para pintar
    pixmap = base_icon.pixmap(size, size)
    
    if pixmap.isNull():
        return QIcon() 

    colored_pixmap = QPixmap(pixmap.size())
    colored_pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(colored_pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(colored_pixmap.rect(), QColor(color))
    painter.end()
    
    return QIcon(colored_pixmap)