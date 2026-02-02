from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
    QHeaderView, QMessageBox, QFormLayout, QFileDialog
)
from PyQt6.QtCore import Qt

# --- IMPORTACIONES MODULARES ---
from logic_medicos import LogicaMedicos
from data_services import ServicioDatos
import theme
import utils

class WidgetConsultar(QWidget):
    def __init__(self):
        super().__init__()
        # Instancias de lógica y servicios
        self.logic = LogicaMedicos()
        self.data_service = ServicioDatos()
        
        self.id_seleccionado = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # --- HEADER ---
        header = QHBoxLayout()
        lbl_titulo = QLabel("Gestión de Médicos")
        lbl_titulo.setObjectName("h1")
        header.addWidget(lbl_titulo)
        header.addStretch()
        self.layout.addLayout(header)

        # --- BARRA DE FILTROS ---
        frame_filtros = QFrame()
        frame_filtros.setStyleSheet(theme.STYLES["card"])
        layout_filtros = QHBoxLayout(frame_filtros)
        layout_filtros.setContentsMargins(10, 10, 10, 10)

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Buscar...")
        self.txt_buscar.textChanged.connect(self.cargar_datos)

        self.filtro_esp = QComboBox()
        self.filtro_esp.setStyleSheet(theme.STYLES["combobox"])
        self.filtro_esp.addItem("Todas las Especialidades")
        self.filtro_esp.addItems(["Medicina General", "Cardiología", "Pediatría", "Dermatología", "Neurología"])
        self.filtro_esp.currentTextChanged.connect(self.cargar_datos)

        # --- BOTONES DE ACCIÓN ---
        btn_exportar = QPushButton("Exportar CSV")
        btn_exportar.setIcon(utils.get_icon("upload.svg", color="white")) 
        btn_exportar.setStyleSheet(theme.STYLES["btn_primary"])
        btn_exportar.clicked.connect(self.manejar_exportacion) # <--- Nombre más descriptivo

        btn_importar = QPushButton("Importar CSV")
        btn_importar.setIcon(utils.get_icon("download.svg", color=theme.Palette.Text_Secondary)) 
        btn_importar.setStyleSheet(theme.STYLES["btn_icon_ghost"])
        btn_importar.clicked.connect(self.manejar_importacion) # <--- Nombre más descriptivo

        btn_refrescar = QPushButton()
        btn_refrescar.setIcon(utils.get_icon("refresh.svg", color=theme.Palette.Action_Blue))
        btn_refrescar.setStyleSheet(theme.STYLES["btn_icon_ghost"])
        btn_refrescar.setToolTip("Recargar Tabla")
        btn_refrescar.clicked.connect(self.cargar_datos)

        layout_filtros.addWidget(self.txt_buscar, 2)
        layout_filtros.addWidget(self.filtro_esp, 1)
        layout_filtros.addWidget(btn_importar)
        layout_filtros.addWidget(btn_exportar)
        layout_filtros.addWidget(btn_refrescar)
        
        self.layout.addWidget(frame_filtros)

        # --- TABLA ---
        self.tabla = QTableWidget()
        self.columnas = ["Nombres", "Apellidos", "Especialidad", "Tel 1", "Tel 2", "Dirección", "Estado", "Acciones"]
        self.tabla.setColumnCount(len(self.columnas))
        self.tabla.setHorizontalHeaderLabels(self.columnas)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.tabla.setColumnWidth(7, 100)
        self.layout.addWidget(self.tabla)

        self.setup_edicion_form()
        self.cargar_datos()

    def setup_edicion_form(self):
        self.frame_edicion = QFrame()
        self.frame_edicion.setStyleSheet(f"background: {theme.Palette.Focus_Bg}; border-top: 1px solid {theme.Palette.Border};")
        
        main_layout = QVBoxLayout(self.frame_edicion)
        
        lbl_edit = QLabel("Editando Información:")
        lbl_edit.setStyleSheet(f"font-weight: bold; color: {theme.Palette.Primary};")
        main_layout.addWidget(lbl_edit)
        
        form_layout = QFormLayout()
        
        self.edit_nombres = QLineEdit()
        self.edit_apellidos = QLineEdit()
        self.edit_especialidad = QComboBox()
        self.edit_especialidad.setStyleSheet(theme.STYLES["combobox"])
        self.edit_especialidad.addItems(["Medicina General", "Cardiología", "Pediatría", "Dermatología", "Neurología"])
        
        self.edit_tel1 = QLineEdit()
        self.edit_tel2 = QLineEdit()
        # Validación visual al editar también
        self.edit_tel1.textChanged.connect(lambda: self.validar_numeros_visual(self.edit_tel1))
        self.edit_tel2.textChanged.connect(lambda: self.validar_numeros_visual(self.edit_tel2))

        self.edit_direccion = QLineEdit()
        self.edit_estado = QComboBox()
        self.edit_estado.setStyleSheet(theme.STYLES["combobox"])
        self.edit_estado.addItems(["Activo", "Inactivo", "Vacaciones", "Licencia"])
        
        form_layout.addRow("Nombres:", self.edit_nombres)
        form_layout.addRow("Apellidos:", self.edit_apellidos)
        form_layout.addRow("Especialidad:", self.edit_especialidad)
        form_layout.addRow("Teléfono 1:", self.edit_tel1)
        form_layout.addRow("Teléfono 2:", self.edit_tel2)
        form_layout.addRow("Dirección:", self.edit_direccion)
        form_layout.addRow("Estado:", self.edit_estado)
        
        main_layout.addLayout(form_layout)

        btns = QHBoxLayout()
        btn_save = QPushButton(" Guardar Cambios")
        btn_save.setIcon(utils.get_icon("save.svg", color="white"))
        btn_save.setStyleSheet(theme.STYLES["btn_primary"])
        btn_save.clicked.connect(self.guardar_cambios)

        btn_cancel = QPushButton(" Cancelar")
        btn_cancel.setStyleSheet(theme.STYLES["btn_icon_ghost"])
        btn_cancel.clicked.connect(lambda: self.frame_edicion.hide())
        
        btns.addStretch()
        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        main_layout.addLayout(btns)
        
        self.layout.addWidget(self.frame_edicion)
        self.frame_edicion.hide()

    def validar_numeros_visual(self, widget):
        texto = widget.text()
        if texto and not texto.isdigit():
            widget.setStyleSheet(f"border: 1px solid {theme.Palette.Danger};")
        else:
            widget.setStyleSheet("")

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        self.frame_edicion.hide()
        
        datos = self.logic.obtener_todos(buscar=self.txt_buscar.text(), filtro_esp=self.filtro_esp.currentText())
        
        for i, row in enumerate(datos):
            self.tabla.insertRow(i)
            id_medico = row[0]
            for col in range(7):
                item = QTableWidgetItem(str(row[col+1]))
                if col == 0: item.setData(Qt.ItemDataRole.UserRole, id_medico)
                self.tabla.setItem(i, col, item)

            w_acc = QWidget()
            l_acc = QHBoxLayout(w_acc)
            l_acc.setContentsMargins(2, 2, 2, 2)
            l_acc.setSpacing(4)
            
            btn_edit = QPushButton()
            btn_edit.setIcon(utils.get_icon("edit.svg", color=theme.Palette.Text_Secondary))
            btn_edit.setToolTip("Editar")
            btn_edit.setStyleSheet(theme.STYLES["btn_icon_ghost"])
            btn_edit.clicked.connect(lambda _, r=i: self.activar_edicion(r))

            btn_del = QPushButton()
            btn_del.setIcon(utils.get_icon("trash.svg", color=theme.Palette.Danger))
            btn_del.setToolTip("Eliminar")
            btn_del.setStyleSheet(f"QPushButton {{ border: none; border-radius: 6px; padding: 4px; }} QPushButton:hover {{ background-color: {theme.Palette.Sidebar_Hover}; }}")
            btn_del.clicked.connect(lambda _, r=i: self.eliminar(r))

            l_acc.addWidget(btn_edit)
            l_acc.addWidget(btn_del)
            self.tabla.setCellWidget(i, 7, w_acc)

    def activar_edicion(self, row):
        self.tabla.selectRow(row)
        item_id = self.tabla.item(row, 0)
        self.id_seleccionado = item_id.data(Qt.ItemDataRole.UserRole)
        
        self.edit_nombres.setText(self.tabla.item(row, 0).text())
        self.edit_apellidos.setText(self.tabla.item(row, 1).text())
        self.edit_especialidad.setCurrentText(self.tabla.item(row, 2).text())
        self.edit_tel1.setText(self.tabla.item(row, 3).text())
        self.edit_tel2.setText(self.tabla.item(row, 4).text())
        self.edit_direccion.setText(self.tabla.item(row, 5).text())
        self.edit_estado.setCurrentText(self.tabla.item(row, 6).text())
        
        self.frame_edicion.show()
        self.tabla.scrollToItem(self.tabla.item(row, 0))

    def guardar_cambios(self):
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
        else:
            QMessageBox.warning(self, "Error al actualizar", msg)

    def eliminar(self, row):
        item = self.tabla.item(row, 0)
        id_m = item.data(Qt.ItemDataRole.UserRole)
        nombre = item.text()
        
        if QMessageBox.question(self, "Confirmar", f"¿Eliminar a {nombre}?") == QMessageBox.StandardButton.Yes:
            self.logic.eliminar_medico(id_m)
            self.cargar_datos()

    # --- LÓGICA DE EXPORTACIÓN LIMPIA ---
    def manejar_exportacion(self):
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Médicos", "", "Archivos CSV (*.csv)")
        if not archivo: return
        
        # 1. Obtener datos de la lógica
        datos = self.logic.obtener_todos()
        
        # 2. Usar servicio de datos para escribir
        exito, msg = self.data_service.exportar_csv(archivo, datos, self.columnas)
        
        if exito:
            QMessageBox.information(self, "Exportar", msg)
        else:
            QMessageBox.critical(self, "Error", msg)

    # --- LÓGICA DE IMPORTACIÓN LIMPIA ---
    def manejar_importacion(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Importar Médicos", "", "Archivos CSV (*.csv)")
        if not archivo: return
        
        # 1. Usar servicio de datos para leer
        filas, error = self.data_service.importar_csv(archivo)
        
        if error:
            QMessageBox.warning(self, "Error de Archivo", error)
            return

        # 2. Procesar las filas usando la LÓGICA (Validación incluida)
        exitos, errores = 0, 0
        for row in filas:
            # row = [Nombre, Apellido, Esp, Tel1, Tel2, Dir, Estado]
            ok, _ = self.logic.crear_medico(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            )
            if ok: exitos += 1
            else: errores += 1
            
        self.cargar_datos()
        QMessageBox.information(self, "Importación Finalizada", 
                              f"✅ Registros creados: {exitos}\n"
                              f"⚠️ Registros inválidos omitidos: {errores}")