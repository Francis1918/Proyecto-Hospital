# Pacientes/views/consultar_view.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLabel, QLineEdit, 
    QHeaderView, QMessageBox, QAbstractItemView, QFrame, QComboBox
)
from PyQt6.QtCore import Qt

# Imports del Core
from core.theme import AppPalette, STYLES
from core.utils import get_icon

# Imports del Módulo
# Nota: Asumimos que los diálogos de edición siguen en su carpeta original o dialogs.py
# Si moviste DetallePacienteDialog, ajusta este import.
# Por ahora, dejaremos pendiente la importación del Detalle para integrarlo después.
from Pacientes.dialogs.historia_clinica_dialog import HistoriaClinicaDialog

class ConsultarPacienteView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.pacientes_lista = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # --- 1. BARRA DE BÚSQUEDA (Tarjeta Superior) ---
        search_frame = QFrame()
        search_frame.setStyleSheet(STYLES["card"])
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(20, 15, 20, 15)
        search_layout.setSpacing(15)

        search_layout.addWidget(QLabel("🔍 Buscar por:"))
        
        self.cmb_filtro = QComboBox()
        self.cmb_filtro.addItems(["Todo", "Cédula", "Nombre", "Apellido"])
        self.cmb_filtro.setFixedWidth(120)
        search_layout.addWidget(self.cmb_filtro)

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Escribe aquí para filtrar...")
        self.txt_buscar.textChanged.connect(self.filtrar_pacientes)
        search_layout.addWidget(self.txt_buscar)

        btn_refresh = QPushButton(" Actualizar")
        btn_refresh.setIcon(get_icon("refresh.svg", AppPalette.text_secondary))
        btn_refresh.setStyleSheet(STYLES["btn_icon_ghost"])
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.clicked.connect(self.cargar_pacientes)
        search_layout.addWidget(btn_refresh)

        layout.addWidget(search_frame)

        # --- 2. TABLA DE PACIENTES (Tarjeta Central) ---
        table_frame = QFrame()
        table_frame.setStyleSheet(STYLES["card"]) # Borde redondeado blanco
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Cédula", "Nombre", "Apellido", "Teléfono", "Email"])
        
        # Configuración de la tabla para que se vea profesional
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.verticalHeader().setVisible(False) # Ocultar números de fila
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setAlternatingRowColors(True)
        # Quitar bordes feos predeterminados y usar el del tema
        self.tabla.setFrameShape(QFrame.Shape.NoFrame) 
        
        # Conectar doble clic para ver detalle
        self.tabla.doubleClicked.connect(self.abrir_detalle)

        table_layout.addWidget(self.tabla)
        layout.addWidget(table_frame)

        # --- 3. BARRA DE ACCIONES (Botones Inferiores) ---
        actions_layout = QHBoxLayout()
        
        self.btn_detalle = QPushButton(" Ver Expediente Completo")
        self.btn_detalle.setIcon(get_icon("file-text.svg", "white"))
        self.btn_detalle.setStyleSheet(STYLES["btn_primary"])
        self.btn_detalle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_detalle.clicked.connect(self.abrir_detalle)

        self.btn_historia = QPushButton(" Historia Clínica")
        self.btn_historia.setIcon(get_icon("activity.svg", AppPalette.text_primary))
        self.btn_historia.setStyleSheet(STYLES["btn_icon_ghost"])
        self.btn_historia.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_historia.clicked.connect(self.abrir_historia)

        self.btn_eliminar = QPushButton(" Eliminar")
        self.btn_eliminar.setIcon(get_icon("trash.svg", AppPalette.Danger))
        # Estilo rojo para peligro
        self.btn_eliminar.setStyleSheet(f"""
            QPushButton {{
                background-color: white; border: 1px solid {AppPalette.Danger}; color: {AppPalette.Danger};
                border-radius: 6px; padding: 8px 16px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #FFF5F5; }}
        """)
        self.btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_eliminar.clicked.connect(self.eliminar_paciente)

        actions_layout.addWidget(self.btn_detalle)
        actions_layout.addWidget(self.btn_historia)
        actions_layout.addStretch()
        actions_layout.addWidget(self.btn_eliminar)

        layout.addLayout(actions_layout)

        # Carga inicial
        self.cargar_pacientes()

    # --- LÓGICA ---
    def cargar_pacientes(self):
        self.pacientes_lista = self.controller.obtener_todos_pacientes()
        self.mostrar_datos(self.pacientes_lista)

    def mostrar_datos(self, pacientes):
        self.tabla.setRowCount(0)
        for p in pacientes:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(p.cc))
            self.tabla.setItem(row, 1, QTableWidgetItem(p.nombre))
            self.tabla.setItem(row, 2, QTableWidgetItem(p.apellido))
            self.tabla.setItem(row, 3, QTableWidgetItem(p.telefono or "-"))
            self.tabla.setItem(row, 4, QTableWidgetItem(p.email or "-"))

    def filtrar_pacientes(self):
        texto = self.txt_buscar.text().strip().lower()
        criterio = self.cmb_filtro.currentText()

        if not texto:
            self.mostrar_datos(self.pacientes_lista)
            return

        filtrados = []
        for p in self.pacientes_lista:
            match = False
            if criterio == "Cédula" and texto in p.cc.lower(): match = True
            elif criterio == "Nombre" and texto in p.nombre.lower(): match = True
            elif criterio == "Apellido" and texto in p.apellido.lower(): match = True
            elif criterio == "Todo":
                if (texto in p.cc.lower() or texto in p.nombre.lower() or texto in p.apellido.lower()):
                    match = True
            
            if match: filtrados.append(p)
        
        self.mostrar_datos(filtrados)

    def get_paciente_seleccionado(self):
        row = self.tabla.currentRow()
        if row < 0: return None
        cc = self.tabla.item(row, 0).text()
        # Buscamos en la lista memoria para tener el objeto completo rápido
        for p in self.pacientes_lista:
            if p.cc == cc: return p
        return None

    def abrir_detalle(self):
        paciente = self.get_paciente_seleccionado()
        if not paciente:
            QMessageBox.warning(self, "Selección", "Seleccione un paciente de la tabla.")
            return
        
        # AQUÍ LLAMAREMOS AL DIÁLOGO DE DETALLE (Lo importaremos dinámicamente o lo crearemos luego)
        # Por ahora mostramos un mensaje temporal si no tienes el archivo
        try:
            # Opción A: Si conservaste el archivo antiguo renombrado
            from Pacientes.dialogs.consultar_paciente_dialog import DetallePacienteDialog
            dlg = DetallePacienteDialog(self.controller, paciente, self)
            dlg.exec()
        except ImportError:
            QMessageBox.information(self, "Detalle", f"Mostrando detalle de {paciente.nombre} (Funcionalidad pendiente de migrar)")

    def abrir_historia(self):
        paciente = self.get_paciente_seleccionado()
        if not paciente:
            QMessageBox.warning(self, "Selección", "Seleccione un paciente.")
            return
            
        dlg = HistoriaClinicaDialog(self.controller, self, paciente=paciente)
        dlg.exec()

    def eliminar_paciente(self):
        paciente = self.get_paciente_seleccionado()
        if not paciente:
            QMessageBox.warning(self, "Selección", "Seleccione un paciente para eliminar.")
            return

        resp = QMessageBox.question(
            self, "Confirmar Eliminación",
            f"¿Está seguro de eliminar a {paciente.nombre} {paciente.apellido}?\nEsta acción es irreversible.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if resp == QMessageBox.StandardButton.Yes:
            ok, msg = self.controller.eliminar_paciente(paciente.cc)
            if ok:
                QMessageBox.information(self, "Éxito", msg)
                self.cargar_pacientes()
            else:
                QMessageBox.warning(self, "Error", msg)