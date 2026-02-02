# Medicos/frontend/utils.py

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt
import theme

def get_icon(filename: str, color: str = None, size: int = 24) -> QIcon:
    """
    Carga un icono SVG/PNG y permite cambiarle el color dinámicamente.
    """
    try:
        path = theme.asset_url(filename)
        base_icon = QIcon(path)
        
        # Si el archivo no existe o está corrupto, QIcon es nulo
        if base_icon.isNull():
            print(f"Advertencia: No se pudo cargar el icono '{filename}' en {path}")
            return QIcon()

        if not color:
            return base_icon

        # Renderizar a Pixmap para pintar
        pixmap = base_icon.pixmap(size, size)
        
        if pixmap.isNull():
            return QIcon() 

        # Crear un lienzo transparente del mismo tamaño
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(colored_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dibujar el icono original
        painter.drawPixmap(0, 0, pixmap)
        
        # Componer el color sobre los píxeles existentes (SourceIn)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(colored_pixmap.rect(), QColor(color))
        painter.end()
        
        return QIcon(colored_pixmap)

    except Exception as e:
        print(f"Error en get_icon para '{filename}': {e}")
        return QIcon()