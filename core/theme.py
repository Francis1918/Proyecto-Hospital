# core/theme.py

# ==========================================
# 1. PALETA UNIFICADA
# ==========================================
class AppPalette:
    # --- COLORES DEL SIDEBAR / MAIN (Estilo Folderly) ---
    white_01        = "#FFFFFF"   # Fondo del sidebar
    white_02        = "#F7FAFC"   # Fondo general de la app
    black_01        = "#1F2937"   # Texto principal (Casi negro)
    black_02        = "#718096"   # Texto secundario (Gris medio)
    black_03        = "#A0AEC0"

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
    /* =======================================================
       1. CONFIGURACIÓN BASE
       ======================================================= */
    QMainWindow, QWidget {{ 
        background-color: {c.white_02}; 
        color: {c.black_01}; 
        font-family: "Segoe UI", "Helvetica Neue", sans-serif; 
        font-size: 14px;
    }}

    /* Fix para etiquetas: fondo transparente y sin borde */
    QLabel {{
        border: none;
        background: transparent;
    }}

    /* =======================================================
       2. TIPOGRAFÍA (TÍTULOS)
       ======================================================= */
    QLabel#h1 {{
        color: {c.black_01};
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    QLabel#h2 {{
        color: {c.black_02};
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 5px;
    }}

    /* =======================================================
       3. INPUTS Y FORMULARIOS GENERALES
       (QLineEdit, QComboBox, QDateEdit, QDateTimeEdit)
       ======================================================= */
    QLineEdit, QComboBox, QDateEdit, QDateTimeEdit {{ 
        background-color: {c.Bg_Card}; 
        border: 1px solid {c.Border}; 
        border-radius: 6px; 
        padding: 6px 10px; 
        color: {c.black_01};
        selection-background-color: {c.Focus};
        selection-color: white;
        font-size: 14px;
    }}

    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDateTimeEdit:focus {{ 
        border: 1px solid {c.Focus}; 
        background-color: {c.Bg_Card}; 
    }}
    
    /* Botón flecha desplegable en DateEdit/ComboBox */
    QComboBox::drop-down, QDateEdit::drop-down, QDateTimeEdit::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px; 
        border-left-width: 0px;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
    }}
    
    /* Flecha visual para QDateEdit */
    QDateEdit::down-arrow, QDateTimeEdit::down-arrow {{
        width: 10px;
        height: 10px;
        /* Esto usa el estilo por defecto del sistema operativo si no se define imagen,
           pero asegura que el área sea clicable */
    }}

    /* =======================================================
       4. CALENDARIO (QCalendarWidget)
       ======================================================= */
    
    /* Widget base: Fuente explícita para evitar errores de cálculo */
    QCalendarWidget {{
        font-size: 14px;
    }}

    /* Fondo general */
    QCalendarWidget QWidget {{
        background-color: {c.Bg_Card};
        alternate-background-color: {c.white_02};
        color: {c.black_01};
    }}
    
    /* BOTONES DE NAVEGACIÓN (Mes anterior/siguiente)
       IMPORTANTE: border: 1px solid transparent (reserva espacio)
    */
    QCalendarWidget QToolButton {{
        color: {c.black_01};
        background-color: transparent;
        icon-size: 20px;
        border: 1px solid transparent; 
        border-radius: 4px;
        font-weight: bold;
        margin: 2px;
        font-size: 13px;
        height: 25px; /* Altura fija ayuda a la estabilidad */
        width: 25px;
    }}
    
    QCalendarWidget QToolButton:hover {{
        background-color: {c.hover};
        border: 1px solid {c.Border};
    }}
    
    /* SELECTOR DE AÑO (QSpinBox dentro del calendario)
       IMPORTANTE: Sobrescribimos el padding global para que no rompa el header
    */
    QCalendarWidget QSpinBox {{
        background-color: {c.white_02};
        color: {c.black_01};
        border: 1px solid {c.Border};
        border-radius: 4px;
        margin: 2px;
        font-size: 13px;
        padding-right: 0px; /* <--- CRUCIAL: Quita el padding de los flechas globales */
        selection-background-color: {c.Focus};
        selection-color: white;
        min-width: 60px;
    }}
    
    /* Flechas del SpinBox del año */
    QCalendarWidget QSpinBox::up-button, QCalendarWidget QSpinBox::down-button {{
        subcontrol-origin: border;
        width: 15px;
        border: none;
        background: transparent;
    }}

    QCalendarWidget QSpinBox::up-button:hover, QCalendarWidget QSpinBox::down-button:hover {{
        background-color: {c.hover};
    }}
    
    /* La grilla de días */
    QCalendarWidget QAbstractItemView:enabled {{
        color: {c.black_01};
        background-color: {c.Bg_Card};
        selection-background-color: {c.Focus}; 
        selection-color: white;
        border: none;
        outline: 0;
    }}
    
    QCalendarWidget QAbstractItemView:disabled {{
        color: {c.black_03};
    }}

    /* =======================================================
       3.1 SPINBOXES (NUEVO CÓDIGO AGREGADO)
       ======================================================= */
    QSpinBox, QDoubleSpinBox {{
        background-color: {c.Bg_Card}; 
        color: {c.black_01}; 
        border: 1px solid {c.Border};
        border-radius: 6px;
        padding: 6px 10px; 
        padding-right: 25px; /* Espacio para botones */
        selection-background-color: {c.Focus};
        selection-color: white;
        font-size: 14px;
    }}
    
    QSpinBox:focus, QDoubleSpinBox:focus {{
        background-color: {c.Bg_Card};
        border: 1px solid {c.Focus};
    }}

    /* Botón Arriba */
    QSpinBox::up-button, QDoubleSpinBox::up-button {{
        subcontrol-origin: border; 
        subcontrol-position: top right; 
        width: 20px; 
        border: none;
        border-left: 1px solid {c.Border}; 
        border-top-right-radius: 6px; 
        background-color: {c.Bg_Card};
        margin-top: 1px;
        margin-right: 1px;
    }}
    
    /* Botón Abajo */
    QSpinBox::down-button, QDoubleSpinBox::down-button {{
        subcontrol-origin: border; 
        subcontrol-position: bottom right; 
        width: 20px; 
        border: none;
        border-left: 1px solid {c.Border}; 
        border-bottom-right-radius: 6px; 
        background-color: {c.Bg_Card};
        margin-bottom: 1px;
        margin-right: 1px;
    }}

    /* Hover en los botones */
    QSpinBox::up-button:hover, QSpinBox::down-button:hover,
    QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
        background-color: {c.hover};
    }}

    /* Flechas internas (para asegurar que se vean limpias) */
    QSpinBox::up-arrow, QDoubleSpinBox::up-arrow,
    QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
        width: 8px;
        height: 8px;
        color: {c.black_02};
    }}

    /* =======================================================
       4. CALENDARIO (QCalendarWidget)
       ======================================================= */

    /* =======================================================
       5. PESTAÑAS (QTabWidget)
       ======================================================= */
    QTabWidget::pane {{
        border: 1px solid {c.Border};
        background: {c.Bg_Card};
        border-radius: 6px;
        top: -1px; 
    }}
    QTabBar::tab {{
        background: {c.white_02};
        border: 1px solid {c.Border};
        padding: 8px 20px;
        margin-right: 4px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        color: {c.black_02};
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

    /* =======================================================
       6. TABLAS (QTableWidget)
       ======================================================= */
    QTableWidget {{
        background-color: {c.Bg_Card};
        gridline-color: {c.hover};
        border: 1px solid {c.Border};
        border-radius: 8px;
        selection-background-color: {c.Focus_Bg};
        selection-color: {c.black_01};
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
        background-color: {c.white_02}; 
        color: {c.black_02};
        text-transform: uppercase;
        font-size: 12px;
        font-weight: bold;
        border: none;
        border-bottom: 2px solid {c.Border};
        padding: 12px 6px;
    }}

    /* =======================================================
       7. SCROLLBARS
       ======================================================= */
    QScrollBar:vertical {{
        background: {c.white_02};
        width: 8px;
        margin: 0px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {c.black_03};
        min-height: 20px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {c.black_02};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    /* =======================================================
       8. Comboboxes (QComboBox)
       ======================================================= */   
    QComboBox {{
        background-color: {AppPalette.Bg_Card}; 
        border: 1px solid {AppPalette.Border};
        border-radius: 6px; 
        padding: 6px 12px; 
        color: {AppPalette.black_01};
        font-size: 14px;
    }}
    QComboBox:hover, QComboBox:focus {{ 
        border: 1px solid {AppPalette.Focus}; 
    }}
    QComboBox::drop-down {{ border: none; width: 30px; }}
    
    QComboBox QAbstractItemView {{
        background-color: {AppPalette.Bg_Card};
        border: 1px solid {AppPalette.Border};
        border-radius: 6px; 
        selection-background-color: {AppPalette.Focus_Bg};
        selection-color: {AppPalette.Focus};
        outline: none;
        padding: 4px;
    }}
    QComboBox QAbstractItemView::item {{
        min-height: 30px;
        padding: 0px 8px;
        color: {AppPalette.black_01};
        border: 1px solid {AppPalette.Border};
    }}
    QComboBox QAbstractItemView::item:selected {{
        background-color: {AppPalette.Focus_Bg};
        color: {AppPalette.Focus};
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
            color: {AppPalette.black_02};
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
    "combobox": f"""
        QComboBox {{
            background-color: {AppPalette.Bg_Card}; 
            border: 1px solid {AppPalette.Border};
            border-radius: 6px; 
            padding: 6px 12px; 
            color: {AppPalette.black_01};
            font-size: 14px;
        }}
        QComboBox:hover, QComboBox:focus {{ 
            border: 1px solid {AppPalette.Focus}; 
        }}
        QComboBox::drop-down {{ border: none; width: 30px; }}
        
        QComboBox QAbstractItemView {{
            background-color: {AppPalette.Bg_Card};
            border: 1px solid {AppPalette.Border};
            border-radius: 6px; 
            selection-background-color: {AppPalette.Focus_Bg};
            selection-color: {AppPalette.Focus};
            outline: none;
            padding: 4px;
        }}
        QComboBox QAbstractItemView::item {{
            min-height: 30px;
            padding: 0px 8px;
            color: {AppPalette.black_01};
            border: 1px solid {AppPalette.Border};
        }}
        QComboBox QAbstractItemView::item:selected {{
            background-color: {AppPalette.Focus_Bg};
            color: {AppPalette.Focus};
        }}
    """
}