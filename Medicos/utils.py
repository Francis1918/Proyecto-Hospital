from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt
import theme  # Importamos tu theme para usar asset_url

def get_icon(filename: str, color: str = None, size: int = 24) -> QIcon:
    """
    Carga un icono y cambia su color dinámicamente.
    Ideal para iconos SVG blancos que necesitan verse en fondos claros.
    """
    # Intentamos obtener la ruta desde el theme
    try:
        path = theme.asset_url(filename)
    except AttributeError:
        # Fallback por si theme no tiene asset_url
        return QIcon()

    # 1. Cargar el icono base
    base_icon = QIcon(path)
    
    # Si no especificamos color, devolvemos el original
    if not color:
        return base_icon

    # 2. Renderizar a Pixmap
    pixmap = base_icon.pixmap(size, size)
    
    if pixmap.isNull():
        return QIcon() 

    # 3. Pintar el nuevo color
    colored_pixmap = QPixmap(pixmap.size())
    colored_pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(colored_pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(colored_pixmap.rect(), QColor(color))
    painter.end()
    
    return QIcon(colored_pixmap)