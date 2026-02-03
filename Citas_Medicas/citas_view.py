from datetime import date
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QTabWidget, 
    QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDateEdit, QLineEdit, QMessageBox,
    QAbstractItemView
)
from PyQt6.QtCore import Qt, QSize
from .citas_controller import CitasMedicasController

# Importamos estilos y utilidades
from core.theme import AppPalette, get_sheet, STYLES
from core.utils import get_icon

# Importamos los diálogos
from .dialogs import (
    SolicitarCitaDialog, 
    RegistrarAgendaDialog,
    ModificarCitaDialog,
    EliminarCitaDialog,
    RegistrarEstadoDialog
)

# =======================================================
# 1. PESTAÑA: CONSULTAR CITAS
# =======================================================
class TabConsultarCitas(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._init_ui()

    def _init_ui(self):
        # --- FIX TRANSPARENCIA: Hacemos que este widget sea transparente 
        # para que tome el color BLANCO del QTabWidget::pane ---
        self.setStyleSheet("background-color: transparent;") 
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # -- Filtros --
        filtro_frame = QFrame()
        filtro_frame.setStyleSheet(STYLES["filter_panel"])
        filtro_layout = QHBoxLayout(filtro_frame)

        self.edt_codigo = QLineEdit()
        self.edt_codigo.setPlaceholderText("Código (Ej: CM-ABC123)")
        
        self.edt_cc = QLineEdit()
        self.edt_cc.setPlaceholderText("Cédula Paciente")

        btn_buscar = QPushButton("Buscar")
        btn_buscar.setIcon(get_icon("search.svg", color="white"))
        btn_buscar.setStyleSheet(STYLES["btn_primary"])
        btn_buscar.clicked.connect(self._buscar)

        filtro_layout.addWidget(QLabel("Filtrar por:"))
        filtro_layout.addWidget(self.edt_codigo)
        filtro_layout.addWidget(self.edt_cc)
        filtro_layout.addWidget(btn_buscar)
        layout.addWidget(filtro_frame)

        # -- Tabla --
        self.tabla = QTableWidget(0, 7)
        headers = ["Código", "Paciente", "Especialidad", "Médico", "Fecha", "Hora", "Estado"]
        self.tabla.setHorizontalHeaderLabels(headers)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setAlternatingRowColors(True)
        layout.addWidget(self.tabla)

        # -- Acciones Inferiores --
        actions_layout = QHBoxLayout()
        actions_layout.addWidget(QLabel("<b>Acciones:</b>"))
        
        btn_modificar = QPushButton(" Modificar")
        btn_modificar.setIcon(get_icon("edit.svg", color=AppPalette.text_primary)) 
        btn_modificar.clicked.connect(self._on_modificar)
        
        btn_cancelar = QPushButton(" Cancelar")
        btn_cancelar.setIcon(get_icon("trash.svg", color=AppPalette.Danger)) 
        btn_cancelar.clicked.connect(self._on_cancelar)
        
        btn_estado = QPushButton(" Asistencia")
        btn_estado.setIcon(get_icon("circle-check.svg", color=AppPalette.Success))
        btn_estado.clicked.connect(self._on_estado)

        estilo_acciones = f"""
            QPushButton {{
                background-color: {AppPalette.Bg_Card};
                border: 1px solid {AppPalette.Border};
                color: {AppPalette.text_primary};
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {AppPalette.hover};
                border: 1px solid {AppPalette.Focus};
                color: {AppPalette.Focus};
            }}
            QPushButton:pressed {{
                background-color: {AppPalette.Focus_Bg};
            }}
        """

        for b in [btn_modificar, btn_cancelar, btn_estado]:
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet(estilo_acciones)
            b.setIconSize(QSize(18, 18)) 
            actions_layout.addWidget(b)
        
        actions_layout.addStretch()
        layout.addLayout(actions_layout)

    def _buscar(self):
        codigo = (self.edt_codigo.text() or "").strip()
        cc = (self.edt_cc.text() or "").strip()
        citas = []

        if codigo:
            c = self.controller.consultar_cita_por_codigo(codigo)
            if c: citas = [c]
        elif cc:
            citas = self.controller.consultar_citas_por_paciente(cc)
        else:
            QMessageBox.information(self, "Buscar", "Ingrese Código o Cédula.")
            return

        self.tabla.setRowCount(0)
        if not citas:
            QMessageBox.information(self, "Info", "No se encontraron citas.")
            return

        for c in citas:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            vals = [
                c.codigo, c.nombre_paciente, c.especialidad, 
                c.medico, c.fecha.strftime("%d/%m/%Y"), 
                c.hora.strftime("%H:%M"), c.estado
            ]
            for col, v in enumerate(vals):
                item = QTableWidgetItem(str(v))
                if col == 6: self._color_estado(item, c.estado)
                self.tabla.setItem(row, col, item)

    def _color_estado(self, item, estado):
        colores = {
            "Programada": Qt.GlobalColor.blue,
            "Confirmada": Qt.GlobalColor.blue,
            "Cancelada": Qt.GlobalColor.red,
            "Asistió": Qt.GlobalColor.darkGreen,
            "Tardanza": Qt.GlobalColor.darkYellow
        }
        if estado in colores:
            item.setForeground(colores[estado])
            item.setFont(get_sheet())

    def _get_selected(self):
        row = self.tabla.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selección", "Seleccione una cita de la tabla.")
            return None
        return self.tabla.item(row, 0).text()

    def _on_modificar(self):
        cod = self._get_selected()
        if cod:
            dlg = ModificarCitaDialog(self.controller, self)
            dlg.edt_codigo.setText(cod)
            dlg._cargar()
            if dlg.exec(): self._buscar()

    def _on_cancelar(self):
        cod = self._get_selected()
        if cod:
            dlg = EliminarCitaDialog(self.controller, self)
            dlg.edt_codigo.setText(cod)
            dlg._cargar()
            if dlg.exec(): self._buscar()

    def _on_estado(self):
        cod = self._get_selected()
        if cod:
            dlg = RegistrarEstadoDialog(self.controller, self)
            dlg.edt_codigo.setText(cod)
            dlg._cargar()
            if dlg.exec(): self._buscar()


# =======================================================
# 2. PESTAÑA: CONSULTAR AGENDA
# =======================================================
class TabAgenda(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._init_ui()

    def _init_ui(self):
        # --- FIX TRANSPARENCIA ---
        self.setStyleSheet("background-color: transparent;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        top_frame = QFrame()
        top_frame.setStyleSheet(STYLES["filter_panel"])
        top_layout = QHBoxLayout(top_frame)

        self.cmb_medico = QComboBox()
        self.cmb_medico.setMinimumWidth(200)
        
        self.date_fecha = QDateEdit()
        self.date_fecha.setCalendarPopup(True)
        self.date_fecha.setDate(date.today())
        
        btn_ver = QPushButton("Ver Agenda")
        btn_ver.setIcon(get_icon("calendar.svg", color="white"))
        btn_ver.setStyleSheet(STYLES["btn_primary"])
        btn_ver.clicked.connect(self._consultar)

        top_layout.addWidget(QLabel("Médico:"))
        top_layout.addWidget(self.cmb_medico)
        top_layout.addWidget(QLabel("Fecha:"))
        top_layout.addWidget(self.date_fecha)
        top_layout.addWidget(btn_ver)
        top_layout.addStretch()
        
        layout.addWidget(top_frame)

        self.tabla = QTableWidget(0, 5)
        self.tabla.setHorizontalHeaderLabels(["Hora", "Paciente", "Especialidad", "Estado", "Código Cita"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tabla)
        
        self._cargar_medicos()

    def _cargar_medicos(self):
        self.cmb_medico.clear()
        medicos = self.controller.obtener_todos_medicos()
        for m in medicos:
            self.cmb_medico.addItem(m["nombre_completo"], m["id"])

    def _consultar(self):
        id_medico = self.cmb_medico.currentData()
        if id_medico is None: return
        
        qdate = self.date_fecha.date()
        fecha = date(qdate.year(), qdate.month(), qdate.day())

        citas = self.controller.consultar_agenda(id_medico, fecha)
        self.tabla.setRowCount(0)
        
        if not citas:
            return

        for c in citas:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            vals = [str(c.hora), c.nombre_paciente, c.especialidad, c.estado, c.codigo]
            for col, v in enumerate(vals):
                self.tabla.setItem(row, col, QTableWidgetItem(str(v)))

    def showEvent(self, event):
        self._cargar_medicos()
        super().showEvent(event)


# =======================================================
# 3. PESTAÑA: HISTORIAL NOTIFICACIONES
# =======================================================
class TabNotificaciones(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._init_ui()

    def _init_ui(self):
        # --- FIX TRANSPARENCIA ---
        self.setStyleSheet("background-color: transparent;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("<b>Últimas notificaciones enviadas</b>"))
        top_layout.addStretch()
        
        btn_refresh = QPushButton(" Actualizar")
        btn_refresh.setIcon(get_icon("refresh.svg", color=AppPalette.text_secondary)) 
        btn_refresh.clicked.connect(self._cargar)
        top_layout.addWidget(btn_refresh)
        layout.addLayout(top_layout)

        self.tabla = QTableWidget(0, 6)
        headers = ["Fecha", "Tipo Usuario", "Nombre", "Contacto", "Canal", "Mensaje"]
        self.tabla.setHorizontalHeaderLabels(headers)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tabla)
        
        self._cargar()

    def _cargar(self):
        items = self.controller.obtener_historial_notificaciones()
        self.tabla.setRowCount(0)
        for n in items:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            vals = [
                n.enviada_en.strftime("%Y-%m-%d %H:%M"),
                getattr(n, 'tipo_usuario', '-'),
                getattr(n, 'nombre_destinatario', '-'),
                n.destinatario,
                n.canal,
                n.mensaje
            ]
            for col, v in enumerate(vals):
                self.tabla.setItem(row, col, QTableWidgetItem(str(v)))
    
    def showEvent(self, event):
        self._cargar() 
        super().showEvent(event)


# =======================================================
# VISTA PRINCIPAL (CONTIENE LOS TABS)
# =======================================================
class CitasMedicasView(QMainWindow):
    def __init__(self, controller: CitasMedicasController = None):
        super().__init__()
        self.controller = controller or CitasMedicasController()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gestión de Citas Médicas")
        self.setStyleSheet(get_sheet())

        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0) 

        # --- 1. HEADER ---
        header_frame = QFrame()
        # Se mantiene blanco y redondeado arriba
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppPalette.bg_sidebar}; 
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)

        icon_lbl = QLabel()
        icon_pixmap = get_icon("calendar.svg", color=AppPalette.Primary, size=40).pixmap(40, 40)
        icon_lbl.setPixmap(icon_pixmap)
        
        title_layout = QVBoxLayout()
        lbl_titulo = QLabel("Gestión de Citas Médicas")
        lbl_titulo.setObjectName("h1")
        lbl_subtitulo = QLabel("Programación de consultas, control de agenda y asistencia.")
        lbl_subtitulo.setStyleSheet(f"color: {AppPalette.text_secondary}; font-size: 14px;")
        title_layout.addWidget(lbl_titulo)
        title_layout.addWidget(lbl_subtitulo)

        header_layout.addWidget(icon_lbl)
        header_layout.addSpacing(15)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        btn_solicitar = QPushButton(" Solicitar Nueva Cita")
        btn_solicitar.setIcon(get_icon("plus.svg", color="white"))
        btn_solicitar.setStyleSheet(STYLES["btn_primary"])
        btn_solicitar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_solicitar.clicked.connect(self.abrir_solicitar)
        
        btn_registrar_med = QPushButton(" Configurar Agenda")
        btn_registrar_med.setIcon(get_icon("clipboard.svg", color=AppPalette.text_secondary))
        btn_registrar_med.setStyleSheet(STYLES["btn_icon_ghost"])
        btn_registrar_med.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_registrar_med.clicked.connect(self.abrir_registrar_agenda)

        header_layout.addWidget(btn_registrar_med)
        header_layout.addSpacing(10)
        header_layout.addWidget(btn_solicitar)

        main_layout.addWidget(header_frame)

        # --- 2. TABS ---
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # --- ESTILOS FIX TRANSPARENCIA ---
        self.tabs.setStyleSheet(f"""
            /* 1. Fondo blanco para el widget principal (detrás de los botones) */
            QTabWidget {{
                background-color: {AppPalette.bg_sidebar}; 
            }}
            /* 2. El pane (contenido) blanco y con bordes abajo */
            QTabWidget::pane {{
                border: 1px solid {AppPalette.Border};
                border-top: none; 
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                background-color: {AppPalette.bg_sidebar}; 
            }}
            /* 3. Estilo de los botones de las pestañas */
            QTabBar::tab {{
                background: transparent;
                border: none;
                border-bottom: 2px solid transparent;
                margin-right: 15px;
                padding: 10px 5px;
                font-weight: 600;
                color: {AppPalette.text_secondary};
            }}
            QTabBar::tab:selected {{
                color: {AppPalette.Primary};
                border-bottom: 2px solid {AppPalette.Primary};
            }}
            QTabBar::tab:hover {{
                color: {AppPalette.text_primary};
            }}
        """)

        self.tab_consultar = TabConsultarCitas(self.controller)
        self.tab_agenda = TabAgenda(self.controller)
        self.tab_notif = TabNotificaciones(self.controller)

        self.tabs.addTab(self.tab_consultar, get_icon("search.svg", AppPalette.text_secondary), "Buscar Citas")
        self.tabs.addTab(self.tab_agenda, get_icon("calendar.svg", AppPalette.text_secondary), "Agenda Médicos")
        self.tabs.addTab(self.tab_notif, get_icon("inbox.svg", AppPalette.text_secondary), "Notificaciones")

        main_layout.addWidget(self.tabs)

    # --- Métodos de Acción ---
    def abrir_solicitar(self):
        dlg = SolicitarCitaDialog(self.controller, self)
        if dlg.exec():
            self.tab_consultar._buscar() 
            self.tab_agenda._consultar()

    def abrir_registrar_agenda(self):
        dlg = RegistrarAgendaDialog(self.controller, self)
        if dlg.exec():
            self.tab_agenda._cargar_medicos()