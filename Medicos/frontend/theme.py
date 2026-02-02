# Medicos/frontend/theme.py

import sys
import os

# ==========================================
# 1. SISTEMA DE RUTAS
# ==========================================
def asset_url(filename: str) -> str:
    """Devuelve la ruta absoluta a un recurso (icono/imagen)."""
    if getattr(sys, 'frozen', False):
        # Si es un .exe compilado con PyInstaller
        base_path = sys._MEIPASS
    else:
        # Estructura: Medicos/frontend/theme.py -> subimos 2 niveles a Medicos/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        base_path = project_root
        
    return os.path.join(base_path, "assets", "icons", filename).replace("\\", "/")

# ==========================================
# 2. PALETA DE COLORES (Estilo Dashboard)
# ==========================================
class Palette:
    # Fondos
    Bg_App         = "#F7FAFC"  # Gris muy suave para el fondo de la ventana (como en la imagen)
    Bg_Card        = "#FFFFFF"  # Blanco puro para tarjetas y tablas
    
    # Textos
    Text_Primary   = "#2D3748"  # Gris oscuro casi negro
    Text_Secondary = "#718096"  # Gris medio para etiquetas
    Text_Light     = "#A0AEC0"  # Gris claro para placeholders
    
    # Bordes y Separadores
    Border         = "#E2E8F0"  # Gris suave
    
    # Acciones y Estados
    Primary        = "#00B5D8"  # Cyan/Azul (Similar al botón 'Add Unit' de la imagen)
    Primary_Hover  = "#00A3C4"
    
    Focus          = "#3182CE"  # Azul para focos y selección
    Focus_Bg       = "#EBF8FF"  # Fondo azul muy pálido para items seleccionados
    
    Danger         = "#E53E3E"  # Rojo para eliminar/errores
    Success        = "#38A169"  # Verde para estados activos

# ==========================================
# 3. HOJA DE ESTILOS GLOBAL (QSS)
# ==========================================
def get_sheet() -> str:
    c = Palette
    return f"""
    /* --- CONFIGURACIÓN BASE --- */
    QMainWindow, QWidget {{ 
        background-color: {c.Bg_App}; 
        color: {c.Text_Primary}; 
        font-family: "Segoe UI", "Helvetica Neue", sans-serif; 
        font-size: 14px;
    }}

    /* --- CORRECCIÓN DE LABELS (FIX) --- */
    QLabel {{
        border: none;            /* Quita bordes no deseados */
        background: transparent; /* Fondo transparente */
        padding: 0;
    }}

    /* --- ESTILOS DE TÍTULOS (Ahora funcionan con setObjectName) --- */
    QLabel#h1 {{
        color: {c.Text_Primary};
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    QLabel#h2 {{
        color: {c.Text_Secondary};
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 5px;
    }}

    /* --- PESTAÑAS (TABS) --- */
    QTabWidget::pane {{
        border: 1px solid {c.Border};
        background: {c.Bg_Card};
        border-radius: 6px;
        top: -1px; 
    }}
    QTabBar::tab {{
        background: {c.Bg_App};
        border: 1px solid {c.Border};
        padding: 8px 20px;
        margin-right: 4px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        color: {c.Text_Secondary};
        font-weight: 600;
    }}
    QTabBar::tab:selected {{
        background: {c.Bg_Card};
        color: {c.Focus};
        border-bottom: 2px solid {c.Focus};
    }}
    QTabBar::tab:hover {{
        background: {c.Border};
    }}

    /* --- INPUTS & COMBOS --- */
    QLineEdit, QComboBox {{ 
        background-color: {c.Bg_Card}; 
        border: 1px solid {c.Border}; 
        border-radius: 6px; 
        padding: 6px 10px; 
        color: {c.Text_Primary};
    }}
    QLineEdit:focus, QComboBox:focus {{ 
        border: 1px solid {c.Focus}; 
        background-color: {c.Bg_Card}; 
    }}

    /* --- TABLA --- */
    QTableWidget {{
        background-color: {c.Bg_Card};
        gridline-color: transparent; 
        border: 1px solid {c.Border};
        border-radius: 8px;
        selection-background-color: {c.Focus_Bg};
        selection-color: {c.Text_Primary};
        outline: none;
    }}
    
    QTableWidget::item {{
        padding: 5px;
        border-bottom: 1px solid {c.Border}; 
    }}

    QTableWidget::item:selected {{
        background-color: {c.Focus_Bg};
        color: {c.Focus};
        font-weight: bold;
    }}

    QHeaderView::section {{
        background-color: {c.Bg_App}; 
        color: {c.Text_Secondary};
        text-transform: uppercase;
        font-size: 12px;
        font-weight: bold;
        border: none;
        border-bottom: 2px solid {c.Border};
        padding: 12px 6px;
    }}

    /* --- SCROLLBARS (Opcional, igual que antes) --- */
    QScrollBar:vertical {{
        background: {c.Bg_App};
        width: 8px;
        margin: 0px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {c.Text_Light};
        min-height: 20px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {c.Text_Secondary};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    """

# ==========================================
# 4. COMPONENTES ESPECÍFICOS
# ==========================================
# (Ya quitamos h1 y h2 de aquí porque están en get_sheet)
STYLES = {
    "card": f"""
        QFrame {{
            background-color: {Palette.Bg_Card}; 
            border: 1px solid {Palette.Border}; 
            border-radius: 8px;
        }}
    """,
    "filter_panel": f"""
        QFrame {{
            background-color: {Palette.Bg_Card};
            border-left: 1px solid {Palette.Border};
        }}
        /* Selector específico para evitar conflictos */
        QFrame QLabel {{
            border: none;
            background: transparent;
        }}
    """,
    "btn_primary": f"""
        QPushButton {{ 
            background-color: {Palette.Primary}; 
            color: white; 
            border: none;
            border-radius: 6px; 
            padding: 8px 16px; 
            font-weight: bold; 
            font-size: 13px;
        }}
        QPushButton:hover {{ background-color: {Palette.Primary_Hover}; }}
        QPushButton:pressed {{ background-color: {Palette.Focus}; }}
    """,
    "btn_icon_ghost": f"""
        QPushButton {{ 
            background-color: {Palette.Bg_Card}; 
            color: {Palette.Text_Secondary};
            border: 1px solid {Palette.Border}; 
            border-radius: 6px; 
            padding: 6px; 
        }} 
        QPushButton:hover {{ 
            border: 1px solid {Palette.Focus};
            color: {Palette.Focus};
            background-color: {Palette.Focus_Bg};
        }}
    """,
    "btn_action_dropdown": f"""
        QPushButton {{
            background-color: {Palette.Bg_Card};
            border: 1px solid {Palette.Border};
            border-radius: 4px;
            color: {Palette.Text_Secondary};
            padding: 8px;
            text-align: left;
            font-size: 13px;
        }}
        QPushButton:hover {{
            border-color: {Palette.Focus};
            color: {Palette.Focus};
        }}
        QPushButton::menu-indicator {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 12px;
        }}
    """,
    "menu_dropdown": f"""
        QMenu {{
            background-color: {Palette.Bg_Card};
            border: none;
            border-radius: 6px;
            padding: 4px;
        }}
        QMenu::item {{
            padding: 8px 25px 8px 15px;
            color: {Palette.Text_Primary};
            border-radius: 4px;
        }}
        QMenu::item:selected {{
            background-color: {Palette.Focus_Bg};
            color: {Palette.Focus};
        }}
    """,
    "combobox": f"""
        /* 1. INPUT PRINCIPAL */
        QComboBox {{
            background-color: {Palette.Bg_Card}; 
            border: 1px solid {Palette.Border};
            border-radius: 6px; 
            padding: 6px 12px; 
            color: {Palette.Text_Primary};
            font-size: 14px;
        }}
        
        QComboBox:hover, QComboBox:focus {{ 
            border: 1px solid {Palette.Focus}; 
            background-color: {Palette.Bg_Card};
        }}
        
        QComboBox::drop-down {{ 
            border: none; 
            width: 30px; 
        }}
        
        QComboBox::down-arrow {{
            image: url({asset_url("chevron-down.svg")}); 
            width: 12px; height: 12px;
        }}
        
        /* 2. EL CONTENEDOR DE la LISTA (EL POPUP) */
        QComboBox QAbstractItemView {{
            background-color: {Palette.Bg_Card};
            border: 1px solid {Palette.Border};
            border-radius: 6px; 
            selection-background-color: {Palette.Focus_Bg};
            selection-color: {Palette.Focus};
            outline: none;   /* Quita la línea de foco punteada */
            padding: 4px;    /* Espacio interno general */
        }}

        /* --- AQUÍ ESTÁ EL TRUCO PARA QUITAR BORDES NEGROS --- */
        /* El viewport es el área interna donde viven los items */
        QComboBox QAbstractItemView::viewport {{
            border: none;
            background-color: transparent;
        }}

        /* 3. LOS ITEMS INDIVIDUALES */
        QComboBox QAbstractItemView::item {{
            min-height: 30px;
            padding: 0px 8px;
            border-radius: 4px;
            color: {Palette.Text_Primary};
            border: none; /* Asegura que no tengan borde individual */
        }}
        
        /* Hover y Selección */
        QComboBox QAbstractItemView::item:selected, 
        QComboBox QAbstractItemView::item:hover {{
            background-color: {Palette.Focus_Bg};
            color: {Palette.Focus};
        }}
    """
}
