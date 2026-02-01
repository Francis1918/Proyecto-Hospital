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
    Bg_Main        = "#f0f0f0"  # Blanco puro
    Bg_Soft        = "#f8f9fa"  # Gris muy suave para alternar
    
    # --- Textos ---
    Text_Primary   = "#1a365d"  # Azul oscuro
    Text_Secondary = "#2d3748"  # Gris oscuro
    Text_Light     = "#718096"  # Gris claro

    # --- Sidebar (Azul Corporativo) ---
    Sidebar_Bg     = "#2c5282"  #
    Sidebar_Hover  = "#2b6cb0"  #
    Sidebar_Active = "#2bb5ff"  # Fondo claro seleccionado
    Sidebar_Txt_Active = "#2c5282" 

    # --- Elementos UI ---
    Border         = "#cbd5e0"  #
    Focus          = "#63b3ed"  # Azul brillante
    Focus_Bg       = "#ebf8ff"  #
    
    # --- Acciones ---
    Primary        = "#2c5282"  # Usamos el azul del sidebar como primario
    Action_Blue    = "#5AAEFA"  # Azul botón refrescar
    Danger         = "#e53e3e"  # Rojo error
    Success        = "#48bb78"  # Verde éxito

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
        selection-background-color: {c.Focus_Bg};
        selection-color: {c.Text_Primary};
    }}
    QHeaderView::section {{
        background-color: {c.Bg_Soft};
        color: {c.Text_Primary};
        border: none;
        border-bottom: 2px solid {c.Border};
        padding: 8px;
        font-weight: bold;
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
            padding: 8px 16px; 
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
            padding: 6px; 
        }} 
        QPushButton:hover {{ background-color: {c.Bg_Soft}; }}
    """,

    # Botones del Sidebar (Estilo exacto de estilos.qss)
    "sidebar_btn": f"""
        QPushButton {{
            background-color: transparent; 
            color: white; 
            text-align: left; 
            padding: 12px 20px; 
            border: none; 
            border-left: 4px solid transparent;
            font-size: 14px;
        }}
        QPushButton:hover {{ background-color: {c.Sidebar_Hover}; }}
        QPushButton:checked {{ 
            background-color: {c.Sidebar_Active}; 
            color: {c.Sidebar_Txt_Active}; 
            border-left: 4px solid {c.Primary}; 
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
            background-color: {c.Text_Primary}; 
            color: {c.Bg_Main};
            border: 1px solid {c.Border};
            selection-background-color: {c.Primary}; 
            selection-color: white; 
            outline: none;
            padding: 4px;
        }}
    """
}