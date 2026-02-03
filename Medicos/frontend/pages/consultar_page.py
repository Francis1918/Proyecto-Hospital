# Medicos/frontend/pages/consultar_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
    QHeaderView, QMessageBox, QMenu, QStackedWidget, QFormLayout, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from Medicos.backend.logic_medicos import LogicaMedicos
from Medicos.backend.data_services import ServicioDatos
import core.theme as theme
import core.utils as utils

class WidgetConsultar(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = LogicaMedicos()
        self.data_service = ServicioDatos()
        self.id_seleccionado = None

        # --- LAYOUT PRINCIPAL ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # 1. Header
        self.setup_header()

        # 2. Contenido (Tabla + Panel Lateral)
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(0) 
        
        # Zona Izquierda: Tabla
        self.frame_table = QFrame()
        layout_table_zone = QVBoxLayout(self.frame_table)
        layout_table_zone.setContentsMargins(5, 0, 5, 0)
        
        self.setup_tabla(layout_table_zone)
        self.setup_paginacion(layout_table_zone)

        # Zona Derecha: Panel Lateral (Stack)
        self.side_panel_container = QFrame()
        self.side_panel_container.setFixedWidth(300) 
        self.side_panel_container.setStyleSheet(theme.STYLES["filter_panel"])
        
        self.stack_lateral = QStackedWidget(self.side_panel_container)
        
        # Pag 1: Filtros
        self.page_filtros = QWidget()
        self.setup_filtros_view(self.page_filtros)
        self.stack_lateral.addWidget(self.page_filtros)

        # Pag 2: Edición
        self.page_editar = QWidget()
        self.setup_edicion_view(self.page_editar)
        self.stack_lateral.addWidget(self.page_editar)

        layout_lateral = QVBoxLayout(self.side_panel_container)
        layout_lateral.setContentsMargins(0, 0, 0, 0)
        layout_lateral.addWidget(self.stack_lateral)

        self.content_layout.addWidget(self.frame_table, stretch=1)
        self.content_layout.addWidget(self.side_panel_container)
        self.main_layout.addLayout(self.content_layout)

        # Carga inicial
        self.cargar_datos()

    def setup_header(self):
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 10, 10, 10)

        lbl_titulo = QLabel("Administrar Médicos")
        lbl_titulo.setObjectName("h1")

        self.btn_toggle_panel = QPushButton(" Ocultar Panel")
        self.btn_toggle_panel.setIcon(utils.get_icon("layout.svg", color=theme.AppPalette.black_02))
        self.btn_toggle_panel.setCheckable(True)
        self.btn_toggle_panel.setChecked(True)
        self.btn_toggle_panel.setStyleSheet(theme.STYLES["btn_icon_ghost"])
        self.btn_toggle_panel.clicked.connect(self.toggle_side_panel)

        btn_import = QPushButton(" Importar")
        btn_import.setIcon(utils.get_icon("upload.svg", color=theme.AppPalette.black_02))
        btn_import.setStyleSheet(theme.STYLES["btn_icon_ghost"])
        btn_import.clicked.connect(self.manejar_importacion)

        btn_export = QPushButton(" Exportar CSV")
        btn_export.setIcon(utils.get_icon("download.svg", color="white"))
        btn_export.setStyleSheet(theme.STYLES["btn_primary"])
        btn_export.clicked.connect(self.manejar_exportacion)

        header_layout.addWidget(lbl_titulo)
        header_layout.addStretch()
        header_layout.addWidget(btn_import)
        header_layout.addWidget(btn_export)
        header_layout.addWidget(self.btn_toggle_panel)

        self.main_layout.addWidget(header_frame)

    def setup_tabla(self, layout):
        self.tabla = QTableWidget()
        self.columnas = ["Nombres", "Apellidos", "Especialidad", "Teléfono", "Estado", "Acciones"]
        self.tabla.setColumnCount(len(self.columnas))
        self.tabla.setHorizontalHeaderLabels(self.columnas)
        
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setShowGrid(False)
        self.tabla.setAlternatingRowColors(False)
        
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.tabla.setColumnWidth(5, 110)

        layout.addWidget(self.tabla)

    def setup_paginacion(self, layout):
        bar = QHBoxLayout()
        bar.addStretch()
        
        self.btn_prev = QPushButton("<")
        self.btn_prev.setFixedSize(30, 30)
        self.btn_prev.setStyleSheet(theme.STYLES["btn_icon_ghost"])
        self.btn_prev.clicked.connect(lambda: self.cambiar_pagina(-1))
        
        self.lbl_page = QLabel("1 / 1")
        self.lbl_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_page.setFixedSize(60, 30)
        self.lbl_page.setStyleSheet(f"background: {theme.AppPalette.Focus}; color: white; border-radius: 4px; font-weight: bold;")
        
        self.btn_next = QPushButton(">")
        self.btn_next.setFixedSize(30, 30)
        self.btn_next.setStyleSheet(theme.STYLES["btn_icon_ghost"])
        self.btn_next.clicked.connect(lambda: self.cambiar_pagina(1))

        bar.addWidget(self.btn_prev)
        bar.addWidget(self.lbl_page)
        bar.addWidget(self.btn_next)
        
        layout.addLayout(bar)

    def setup_filtros_view(self, container):
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        header_layout = QHBoxLayout()
        lbl_head = QLabel("FILTROS")
        lbl_head.setStyleSheet(f"color: {theme.AppPalette.black_03}; border: none; background: transparent; font-size: 12px; font-weight: bold;")
        header_layout.addWidget(lbl_head)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        layout.addWidget(QLabel("Buscar:"))
        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Nombre o Apellido...")
        self.txt_buscar.textChanged.connect(self.cargar_datos)
        layout.addWidget(self.txt_buscar)

        layout.addWidget(QLabel("Especialidad:"))
        self.filtro_esp = QComboBox()
        self.filtro_esp.setStyleSheet(theme.STYLES["combobox"])
        self.filtro_esp.addItem("Todas las Especialidades")
        self.filtro_esp.addItems(["Medicina General", "Cardiología", "Pediatría", "Dermatología", "Neurología"])
        self.filtro_esp.currentTextChanged.connect(self.cargar_datos)
        layout.addWidget(self.filtro_esp)

        layout.addWidget(QLabel("Estado:"))
        self.filtro_estado = QComboBox()
        self.filtro_estado.setStyleSheet(theme.STYLES["combobox"])
        self.filtro_estado.addItem("Todos los Estados")
        self.filtro_estado.addItems(["Activo", "Inactivo", "Vacaciones", "Licencia"])
        self.filtro_estado.currentTextChanged.connect(self.cargar_datos)
        layout.addWidget(self.filtro_estado)

        layout.addStretch()

    def setup_edicion_view(self, container):
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        header = QHBoxLayout()
        lbl_head = QLabel("EDITAR MÉDICO")
        lbl_head.setStyleSheet(f"color: {theme.AppPalette.Focus}; font-weight: bold;")
        
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(24, 24)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("background: transparent; border: none; font-weight: bold;")
        btn_close.clicked.connect(self.volver_a_filtros)
        
        header.addWidget(lbl_head)
        header.addStretch()
        header.addWidget(btn_close)
        layout.addLayout(header)

        self.edit_nombres = QLineEdit()
        self.edit_apellidos = QLineEdit()
        self.edit_especialidad = QComboBox()
        self.edit_especialidad.setStyleSheet(theme.STYLES["combobox"])
        self.edit_especialidad.addItems(["Medicina General", "Cardiología", "Pediatría", "Dermatología", "Neurología"])
        
        self.edit_tel1 = QLineEdit()
        self.edit_tel2 = QLineEdit()
        self.edit_direccion = QLineEdit()
        self.edit_estado = QComboBox()
        self.edit_estado.setStyleSheet(theme.STYLES["combobox"])
        self.edit_estado.addItems(["Activo", "Inactivo", "Vacaciones", "Licencia"])

        form = QFormLayout()
        form.setVerticalSpacing(10)
        form.addRow("Nombres:", self.edit_nombres)
        form.addRow("Apellidos:", self.edit_apellidos)
        form.addRow("Especialidad:", self.edit_especialidad)
        form.addRow("Teléfono 1:", self.edit_tel1)
        form.addRow("Teléfono 2:", self.edit_tel2)
        form.addRow("Dirección:", self.edit_direccion)
        form.addRow("Estado:", self.edit_estado)
        layout.addLayout(form)

        layout.addSpacing(10)

        btn_save = QPushButton(" Guardar Cambios")
        btn_save.setIcon(utils.get_icon("save.svg", color="white"))
        btn_save.setStyleSheet(theme.STYLES["btn_primary"])
        btn_save.clicked.connect(self.guardar_cambios_panel)
        layout.addWidget(btn_save)

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(theme.STYLES["btn_icon_ghost"])
        btn_cancel.clicked.connect(self.volver_a_filtros)
        layout.addWidget(btn_cancel)

        layout.addStretch()

    # --- LÓGICA DE UI Y DATOS ---

    def toggle_side_panel(self):
        visible = self.btn_toggle_panel.isChecked()
        if visible:
            self.side_panel_container.show()
            self.btn_toggle_panel.setText(" Ocultar Panel")
        else:
            self.side_panel_container.hide()
            self.btn_toggle_panel.setText(" Mostrar Panel")

    def volver_a_filtros(self):
        self.id_seleccionado = None
        self.stack_lateral.setCurrentIndex(0)

    def cargar_datos(self):
        # Actualiza búsqueda en backend y resetea a página 1
        self.logic.actualizar_busqueda(
            buscar=self.txt_buscar.text(), 
            filtro_esp=self.filtro_esp.currentText(),
            filtro_est=self.filtro_estado.currentText()
        )
        self.mostrar_pagina_actual()

    def cambiar_pagina(self, delta):
        if self.logic.cambiar_pagina(delta):
            self.mostrar_pagina_actual()

    def mostrar_pagina_actual(self):
        self.tabla.setRowCount(0)
        
        datos_pagina = self.logic.obtener_pagina_actual_items()
        
        for i, row in enumerate(datos_pagina):
            self.tabla.insertRow(i)
            id_medico = row[0]
            # [id, nombre, apellido, especialidad, tel1, tel2, dir, estado]
            valores_visuales = [row[1], row[2], row[3], row[4], row[7]]

            for col_idx, valor in enumerate(valores_visuales):
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                if col_idx == 0: 
                    item.setData(Qt.ItemDataRole.UserRole, id_medico)
                self.tabla.setItem(i, col_idx, item)

            self.crear_boton_acciones(i, id_medico, f"{row[1]} {row[2]}")

        # Actualizar UI paginación
        pag, total = self.logic.get_info_paginacion()
        self.lbl_page.setText(f"{pag} / {total}")
        self.btn_prev.setEnabled(pag > 1)
        self.btn_next.setEnabled(pag < total)

    def crear_boton_acciones(self, row, id_medico, nombre_completo):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(2, 0, 2, 0)
        
        btn_action = QPushButton(" Acciones")
        btn_action.setStyleSheet(theme.STYLES["btn_action_dropdown"])
        btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        
        menu = QMenu()
        menu.setStyleSheet(theme.STYLES["menu_dropdown"])
        
        action_edit = QAction("Editar Médico", self)
        action_edit.triggered.connect(lambda: self.cargar_formulario_en_panel(id_medico))
        menu.addAction(action_edit)

        action_del = QAction("Eliminar", self)
        action_del.triggered.connect(lambda: self.eliminar_medico(id_medico, nombre_completo))
        menu.addAction(action_del)
        
        btn_action.setMenu(menu)
        layout.addWidget(btn_action)
        self.tabla.setCellWidget(row, 5, container)

    def cargar_formulario_en_panel(self, id_medico):
        filas = self.logic.obtener_todos_sin_paginar()
        medico = next((m for m in filas if m[0] == id_medico), None)
        
        if not medico: return
        self.id_seleccionado = id_medico
        
        self.edit_nombres.setText(medico[1])
        self.edit_apellidos.setText(medico[2])
        self.edit_especialidad.setCurrentText(medico[3])
        self.edit_tel1.setText(medico[4])
        self.edit_tel2.setText(medico[5])
        self.edit_direccion.setText(medico[6])
        self.edit_estado.setCurrentText(medico[7])

        self.side_panel_container.show()
        self.btn_toggle_panel.setChecked(True)
        self.btn_toggle_panel.setText(" Ocultar Panel")
        self.stack_lateral.setCurrentIndex(1)

    def guardar_cambios_panel(self):
        if not self.id_seleccionado: return

        exito, msg = self.logic.modificar_medico(
            self.id_seleccionado,
            self.edit_nombres.text().strip(),
            self.edit_apellidos.text().strip(),
            self.edit_especialidad.currentText(),
            self.edit_tel1.text().strip(),
            self.edit_tel2.text().strip(),
            self.edit_direccion.text().strip(),
            self.edit_estado.currentText()
        )

        if exito:
            QMessageBox.information(self, "Éxito", msg)
            self.cargar_datos()     
            self.volver_a_filtros()
        else:
            QMessageBox.warning(self, "Error", msg)

    def eliminar_medico(self, id_medico, nombre):
        confirm = QMessageBox.question(
            self, "Confirmar", 
            f"¿Estás seguro de eliminar a {nombre}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.logic.eliminar_medico(id_medico)
            self.cargar_datos()
            if self.id_seleccionado == id_medico:
                self.volver_a_filtros()

    def manejar_exportacion(self):
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Médicos", "", "Archivos CSV (*.csv)")
        if not archivo: return
        
        datos = self.logic.obtener_todos_sin_paginar()
        exito, msg = self.data_service.exportar_csv(archivo, datos, self.columnas)
        if exito:
            QMessageBox.information(self, "Exportar", msg)
        else:
            QMessageBox.critical(self, "Error", msg)
            
    def manejar_importacion(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Importar Médicos", "", "Archivos CSV (*.csv)")
        if not archivo: return
        
        filas, error = self.data_service.importar_csv(archivo)
        if error:
            QMessageBox.warning(self, "Error", error)
            return

        exitos = 0
        errores = 0
        for row in filas:
            ok, _ = self.logic.crear_medico(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            )
            if ok: exitos += 1
            else: errores += 1
            
        self.cargar_datos()
        QMessageBox.information(self, "Importación", f"Proceso finalizado.\nImportados: {exitos}\nFallidos: {errores}")