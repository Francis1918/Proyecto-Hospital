import sys
import os

# ==========================================
# 1. SISTEMA DE RUTAS
# ==========================================
def asset_url(filename: str) -> str:
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # Asume que theme.py está en la carpeta Medicos/
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "assets", "icons", filename).replace("\\", "/")

# ==========================================
# 2. PALETA ORIGINAL (Basada en estilos.qss)
# ==========================================
class Palette:
    # --- Fondos ---
    Bg_Main        = "#FFFFFF"  # Contenido blanco puro
    
    # --- Sidebar (Gris muy suave, casi blanco) ---
    Sidebar_Bg     = "#7C93C1"
    Sidebar_Hover  = "#E2E2E2"
    Sidebar_Active = "#EAEAEA"
    Sidebar_Txt_Active = "#000000"

    # --- Textos ---
    Text_Primary   = "#1A202C"  # Negro suave (Casi negro)
    Text_Secondary = "#718096"  # Gris para iconos o textos secundarios
    Text_Light     = "#A0AEC0"  # Gris muy claro (para versiones, footers)

    # --- Elementos UI ---
    Border         = "#E2E8F0"  # Bordes muy sutiles
    Focus          = "#3182CE"  
    Focus_Bg       = "#EBF8FF"  
    
    # --- Acciones ---
    Primary        = "#1A202C"  # Botones principales negros (estilo minimalista) o azul si prefieres
    Action_Blue    = "#3182CE"  
    Danger         = "#E53E3E"  
    Success        = "#38A169"

# ==========================================
# 3. HOJA DE ESTILOS GLOBAL (QSS)
# ==========================================
def get_sheet() -> str:
    c = Palette
    return f"""
    /* --- BASE --- */
    QMainWindow, QWidget {{ 
        background-color: {c.Bg_Main}; 
        color: {c.Text_Primary}; 
        font-family: "Segoe UI", sans-serif; font-size: 14px;
    }}
    
    /* --- SIDEBAR --- */
    QFrame#Sidebar {{ 
        background-color: {c.Sidebar_Bg}; 
        border: none; 
    }}
    
    /* --- TEXTOS --- */
    QLabel#h1 {{ 
        font-size: 22px; font-weight: bold; color: {c.Text_Primary}; 
        padding: 0px; margin-bottom: 10px;
    }}
    QLabel#h2 {{ 
        font-size: 16px; font-weight: bold; color: {c.Bg_Main}; 
        padding: 0px;
    }}
    
    /* --- INPUTS --- */
    QLineEdit, QComboBox {{ 
        background-color: {c.Bg_Main}; 
        border: 1px solid {c.Border}; 
        border-radius: 6px; padding: 6px; 
        color: {c.Text_Secondary};
    }}
    QLineEdit:focus, QComboBox:focus {{ 
        border: 1px solid {c.Focus}; 
        background-color: {c.Focus_Bg}; 
    }}

    /* --- TABLA --- */
    QTableWidget {{
        background-color: {c.Bg_Main};
        gridline-color: {c.Border};
        border: 1px solid {c.Border};
        border-radius: 8px;
        outline: none; /* Quita la línea punteada fea al seleccionar */
    }}

    /* Estilo de la celda cuando está SELECCIONADA */
    QTableWidget::item:selected {{
        background-color: {c.Focus}; /* Usamos el azul fuerte (#3182CE) para que se note */
        color: white;               /* Texto blanco */
        border: none;
    }}

    /* Estilo de la selección cuando la tabla PIERDE EL FOCO (ej. al tocar botones) */
    QTableWidget::item:selected:!active {{
        background-color: {c.Focus};
        color: white;
    }}

    QHeaderView::section {{
        background-color: {c.Sidebar_Bg};
        color: {c.Text_Primary};
        border: none;
        border-bottom: 1px solid {c.Border};
        padding: 10px;
        font-weight: 600;
    }}
    QHeaderView::section {{
        background-color: {c.Sidebar_Hover};
        color: {c.Text_Primary};
        border: none;
        border-bottom: 2px solid {c.Border};
        padding: 8px;
        font-weight: bold;
    }}

    /* --- SCROLLBAR VERTICAL --- */
    QScrollBar:vertical {{
        border: none;
        background: {c.Focus_Bg};
        width: 10px;
        margin: 12px 0px 12px 0px;
    }}
    
    /* La barra que se mueve (Handle) */
    QScrollBar::handle:vertical {{
        background: {c.Focus};
        min-height: 30px;
        border-radius: 5px;
    }}
    
    /* Efecto Hover en la barra */
    QScrollBar::handle:vertical:hover {{
        background: {c.Text_Light};
    }}

    /* Botón de Arriba (sub-line) */
    QScrollBar::sub-line:vertical {{
        border: none;
        background: {c.Focus};
        height: 16px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }}

    /* Botón de Abajo (add-line) */
    QScrollBar::add-line:vertical {{
        border: none;
        background: {c.Focus};
        height: 16px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }}

    QScrollBar::sub-line:vertical:hover, QScrollBar::add-line:vertical:hover {{
        background: {c.Focus_Bg};
    }}

    /* --- ICONOS DE LAS FLECHAS --- */
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
        width: 12px;
        height: 12px;
    }}

    QScrollBar::up-arrow:vertical {{
        image: url({asset_url("chevron-up.svg")});
    }}

    QScrollBar::down-arrow:vertical {{
        image: url({asset_url("chevron-down.svg")});
    }}
    /* Fondo cuando no hay barra */
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}

    /* --- SCROLLBAR HORIZONTAL --- */
    QScrollBar:horizontal {{
        border: none;
        background: {c.Focus_Bg}; /* Fondo sutil (gris muy claro) */
        height: 10px;            /* Altura delgada */
        margin: 0px 0px 0px 0px;
        border-radius: 0px;
    }}
    
    QScrollBar::handle:horizontal {{
        background: {c.Focus};
        min-width: 30px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: {c.Text_Light};
    }}
    
    QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal {{
        border: none;
        background: none;
        width: 0px;
    }}
    
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
        background: none;
    }}
    """
    
# ==========================================
# 4. COMPONENTES ESPECÍFICOS
# ==========================================
c = Palette

STYLES = {
    # Tarjetas (Fondo blanco con borde suave)
    "card": f"""
        QFrame {{
            background-color: {c.Bg_Main}; 
            border: 1px solid {c.Border}; 
            border-radius: 10px;
        }}
    """,

    # Botón Principal (Azul Sólido)
    "btn_primary": f"""
        QPushButton {{ 
            background-color: {c.Primary}; 
            color: white; 
            border-radius: 6px; 
            padding: 8px; 
            font-weight: bold; 
        }}
        QPushButton:hover {{ background-color: {c.Sidebar_Hover}; }}
    """,
    
    # Botón de Icono (Fantasma)
    "btn_icon_ghost": f"""
        QPushButton {{ 
            background-color: transparent; 
            border: 1px solid {c.Border}; 
            border-radius: 6px; 
            padding: 8px; 
        }} 
        QPushButton:hover {{ background-color: {c.Sidebar_Hover}; }}
    """,

    # Botones del Sidebar (Estilo exacto de estilos.qss)
    "sidebar_btn": f"""
        QPushButton {{
            background-color: transparent; 
            color: {c.Bg_Main}; 
            text-align: left; 
            padding: 10px 15px; 
            border: none; 
            border-radius: 8px; /* Bordes redondeados */
            font-size: 14px;
            margin: 2px 10px; /* Margen para que el botón no toque los bordes del sidebar */
        }}
        QPushButton:hover {{ 
            background-color: {c.Sidebar_Hover}; 
            color: {c.Text_Primary};
        }}
        QPushButton:checked {{ 
            background-color: {c.Sidebar_Active}; /* Fondo gris suave */
            color: {c.Sidebar_Txt_Active}; 
            font-weight: bold; 
        }}
    """,
    
    "combobox": f"""
        QComboBox {{
            background-color: {c.Bg_Main}; 
            border: 1px solid {c.Border};
            color: {c.Text_Primary}; 
            border-radius: 6px; 
            padding: 6px 12px; 
            min-height: 16px;
        }}
        
        /* Efecto al pasar el mouse o dar click */
        QComboBox:hover, QComboBox:focus {{
            border: 1px solid {c.Focus}; 
            background-color: {c.Focus_Bg};
        }}
        
        /* Quitar el borde estándar del botón de la flecha */
        QComboBox::drop-down {{ 
            border: none; 
            width: 30px; /* Espacio para la flecha */
        }}

        /* Flecha personalizada (Reposo) */
        QComboBox::down-arrow {{
            image: url({asset_url("chevron-down.svg")}); 
            width: 12px; 
            height: 12px;
        }}
        
        /* Flecha personalizada (Cuando se abre el menú) */
        QComboBox::down-arrow:on {{
            image: url({asset_url("chevron-up.svg")});
        }}

        /* Estilo de la lista desplegable (El menú que se abre) */
        QComboBox QAbstractItemView {{
            background-color: {c.Focus}; 
            color: {c.Bg_Main};
            border: 1px solid {c.Border};
            selection-background-color: {c.Primary}; 
            selection-color: white; 
            outline: none;
            padding: 4px;
        }}
    """
}