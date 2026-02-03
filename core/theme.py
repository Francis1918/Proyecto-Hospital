# core/theme.py

# ==========================================
# 1. PALETA UNIFICADA
# ==========================================
class AppPalette:
    # --- COLORES DEL SIDEBAR / MAIN (Estilo Folderly) ---
    bg_main       = "#F7FAFC"   # Fondo general de la app
    bg_sidebar    = "#FFFFFF"   # Fondo del sidebar
    text_primary  = "#1F2937"   # Texto principal (Casi negro)
    text_secondary= "#718096"   # Texto secundario (Gris medio)
    text_light    = "#A0AEC0"

    # --- COLORES INTERNOS / ACCIONES ---
    Primary       = "#00B5D8"   # Cyan/Azul Principal
    Primary_Hover = "#00A3C4"
    Focus         = "#3182CE"   # Azul Fuerte (Selección)
    Focus_Bg      = "#EBF8FF"   # Fondo azul claro (Items seleccionados)
    
    # --- ESTADOS ---
    Danger        = "#E53E3E"
    Success       = "#38A169"
    Border        = "#E2E8F0"   # Bordes suaves
    Bg_Card       = "#FFFFFF"   # Fondo de tarjetas
    
    # --- UTILIDADES ---
    hover         = "#F7FAFC"   # Hover genérico
    active_bg     = "#EFF6FF"   # Fondo activo sidebar
    active_text   = "#3182CE"   # Texto activo sidebar

# ==========================================
# 2. ESTILOS GLOBALES (QSS)
# ==========================================
def get_sheet() -> str:
    c = AppPalette
    return f"""
    /* --- CONFIGURACIÓN BASE --- */
    QMainWindow, QWidget {{ 
        background-color: {c.bg_main}; 
        color: {c.text_primary}; 
        font-family: "Segoe UI", "Helvetica Neue", sans-serif; 
        font-size: 14px;
    }}

    /* --- CORRECCIÓN DE LABELS (FIX) --- */
    QLabel {{
        border: none;            /* Quita bordes no deseados */
        background: transparent; /* Fondo transparente */
    }}

    /* --- ESTILOS DE TÍTULOS (Ahora funcionan con setObjectName) --- */
    QLabel#h1 {{
        color: {c.text_primary};
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    QLabel#h2 {{
        color: {c.text_secondary};
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
        background: {c.bg_main};
        border: 1px solid {c.Border};
        padding: 8px 20px;
        margin-right: 4px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        color: {c.text_secondary};
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
        color: {c.text_primary};
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
        selection-color: {c.text_primary};
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
        background-color: {c.bg_main}; 
        color: {c.text_secondary};
        text-transform: uppercase;
        font-size: 12px;
        font-weight: bold;
        border: none;
        border-bottom: 2px solid {c.Border};
        padding: 12px 6px;
    }}


    /* --- SCROLLBARS (Opcional, igual que antes) --- */
    QScrollBar:vertical {{
        background: {c.bg_main};
        width: 8px;
        margin: 0px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {c.text_light};
        min-height: 20px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {c.text_secondary};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    """


# ==========================================
# 3. ESTILOS ESPECÍFICOS (COMPONENTES)
# ==========================================
STYLES = {
    "card": f"""
        QFrame {{
            background-color: {AppPalette.Bg_Card}; 
            border: 1px solid {AppPalette.Border}; 
            border-radius: 8px;
        }}
    """,
    "filter_panel": f"""
        QFrame {{
            background-color: {AppPalette.Bg_Card};
            border-left: 1px solid {AppPalette.Border};
        }}
        /* Selector específico para evitar conflictos */
        QFrame QLabel {{
            border: none;
            background: transparent;
        }}
    """,
    "btn_primary": f"""
        QPushButton {{ 
            background-color: {AppPalette.Primary}; 
            color: white; 
            border: none;
            border-radius: 6px; 
            padding: 8px 16px; 
            font-weight: bold; 
            font-size: 13px;
        }}
        QPushButton:hover {{ background-color: {AppPalette.Primary_Hover}; }}
        QPushButton:pressed {{ background-color: {AppPalette.Focus}; }}
    """,
    "btn_icon_ghost": f"""
        QPushButton {{ 
            background-color: {AppPalette.Bg_Card}; 
            color: {AppPalette.text_secondary};
            border: 1px solid {AppPalette.Border}; 
            border-radius: 6px; 
            padding: 6px; 
        }} 
        QPushButton:hover {{ 
            border: 1px solid {AppPalette.Focus};
            color: {AppPalette.Focus};
            background-color: {AppPalette.Focus_Bg};
        }}
    """,
    "btn_action_dropdown": f"""
        QPushButton {{
            background-color: {AppPalette.Bg_Card};
            border: 1px solid {AppPalette.Border};
            border-radius: 4px;
            color: {AppPalette.text_secondary};
            padding: 8px;
            text-align: left;
            font-size: 13px;
        }}
        QPushButton:hover {{
            border-color: {AppPalette.Focus};
            color: {AppPalette.Focus};
        }}
        QPushButton::menu-indicator {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 12px;
        }}
    """,
    "menu_dropdown": f"""
        QMenu {{
            background-color: {AppPalette.Bg_Card};
            border: none;
            border-radius: 6px;
            padding: 4px;
        }}
        QMenu::item {{
            padding: 8px 25px 8px 15px;
            color: {AppPalette.text_primary};
            border-radius: 4px;
        }}
        QMenu::item:selected {{
            background-color: {AppPalette.Focus_Bg};
            color: {AppPalette.Focus};
        }}
    """,
    "combobox": f"""
        /* 1. INPUT PRINCIPAL */
        QComboBox {{
            background-color: {AppPalette.Bg_Card}; 
            border: 1px solid {AppPalette.Border};
            border-radius: 6px; 
            padding: 6px 12px; 
            color: {AppPalette.text_primary};
            font-size: 14px;
        }}
        
        QComboBox:hover, QComboBox:focus {{ 
            border: 1px solid {AppPalette.Focus}; 
            background-color: {AppPalette.Bg_Card};
        }}
        
        QComboBox::drop-down {{ 
            border: none; 
            width: 30px; 
        }}
        
        /* 2. EL CONTENEDOR DE la LISTA (EL POPUP) */
        QComboBox QAbstractItemView {{
            background-color: {AppPalette.Bg_Card};
            border: 1px solid {AppPalette.Border};
            border-radius: 6px; 
            selection-background-color: {AppPalette.Focus_Bg};
            selection-color: {AppPalette.Focus};
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
            color: {AppPalette.text_primary};
            border: none; /* Asegura que no tengan borde individual */
        }}
        
        /* Hover y Selección */
        QComboBox QAbstractItemView::item:selected, 
        QComboBox QAbstractItemView::item:hover {{
            background-color: {AppPalette.Focus_Bg};
            color: {AppPalette.Focus};
        }}
    """
}