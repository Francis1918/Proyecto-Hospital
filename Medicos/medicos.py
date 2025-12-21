import sys
import csv
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QFormLayout, QFrame, 
                             QStackedWidget)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

# Nombre del archivo CSV
ARCHIVO_DB = 'Medicos/medicos.csv'
ARCHIVO_ESTILOS = 'Medicos/estilos.qss'

# ----------------------------------------------------------------
# CLASE 1: REGISTRAR MÉDICO
# ----------------------------------------------------------------
class WidgetRegistrar(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializar_csv()
        
        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        titulo = QLabel("🟦 Registrar Nuevo Médico")
        titulo.setObjectName("titulo_page") # ID para CSS
        self.layout_principal.addWidget(titulo)

        # Frame del formulario
        form_frame = QFrame()
        form_frame.setObjectName("form_card") # ID para CSS
        
        layout_form = QFormLayout(form_frame)
        layout_form.setSpacing(15)
        layout_form.setContentsMargins(20, 20, 20, 20)

        # Campos
        self.txt_nombres = QLineEdit()
        self.txt_apellidos = QLineEdit()
        
        self.cb_especialidad = QComboBox()
        self.cb_especialidad.addItems(["Seleccione", "Medicina General", "Cardiología", "Pediatría", "Dermatología", "Neurología"])
        
        # --- Teléfonos Dinámicos ---
        self.container_telefonos = QWidget()
        self.layout_telefonos = QVBoxLayout(self.container_telefonos)
        self.layout_telefonos.setContentsMargins(0,0,0,0)
        
        # Primer teléfono obligatorio
        self.txt_tel1 = self.crear_input_telefono()
        self.layout_telefonos.addWidget(self.txt_tel1)
        
        # Botón para agregar extra
        self.btn_add_tel = QPushButton("+ Agregar otro teléfono")
        self.btn_add_tel.setObjectName("btnAddTel") # ID para CSS
        self.btn_add_tel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_tel.clicked.connect(self.agregar_telefono_extra)
        self.layout_telefonos.addWidget(self.btn_add_tel)

        # Resto de campos
        self.txt_direccion = QLineEdit()
        self.cb_estado = QComboBox()
        self.cb_estado.addItems(["Seleccione", "Activo", "Inactivo", "Vacaciones", "Licencia"])

        # Agregar al layout
        layout_form.addRow("Nombres:", self.txt_nombres)
        layout_form.addRow("Apellidos:", self.txt_apellidos)
        layout_form.addRow("Especialidad:", self.cb_especialidad)
        layout_form.addRow("Teléfono(s):", self.container_telefonos)
        layout_form.addRow("Dirección:", self.txt_direccion)
        layout_form.addRow("Estado:", self.cb_estado)

        self.layout_principal.addWidget(form_frame)

        # Botón Guardar
        btn_guardar = QPushButton("Guardar Médico")
        btn_guardar.setObjectName("btnGuardar") # ID para CSS
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.setFixedHeight(45)
        btn_guardar.clicked.connect(self.guardar_datos)
        self.layout_principal.addWidget(btn_guardar)
        self.layout_principal.addStretch()

        self.inputs_extra_telefonos = [] 

    def inicializar_csv(self):
        if not os.path.exists(ARCHIVO_DB):
            with open(ARCHIVO_DB, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Nombres", "Apellidos", "Especialidad", "Teléfono 1", "Teléfono 2", "Dirección", "Estado"])

    def crear_input_telefono(self):
        txt = QLineEdit()
        txt.setPlaceholderText("Solo números...")
        txt.textChanged.connect(lambda: self.validar_numeros(txt))
        return txt

    def agregar_telefono_extra(self):
        if len(self.inputs_extra_telefonos) < 1: 
            nuevo_tel = self.crear_input_telefono()
            self.inputs_extra_telefonos.append(nuevo_tel)
            self.layout_telefonos.insertWidget(self.layout_telefonos.count()-1, nuevo_tel)
        else:
            QMessageBox.information(self, "Aviso", "Máximo 2 teléfonos permitidos.")

    def validar_numeros(self, widget):
        texto = widget.text()
        if texto and not texto.isdigit():
            self.set_status(widget, "error")
        else:
            self.set_status(widget, "normal")

    def set_status(self, widget, status):
        widget.setProperty("status", status)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def flash_verde(self):
        widgets = [self.txt_nombres, self.txt_apellidos, self.cb_especialidad, 
                   self.txt_tel1, self.txt_direccion, self.cb_estado] + self.inputs_extra_telefonos
        
        for w in widgets:
            self.set_status(w, "success")
        
        QTimer.singleShot(800, lambda: [self.set_status(w, "normal") for w in widgets])

    def guardar_datos(self):
        errores = False

        # Validaciones
        text_fields = [self.txt_nombres, self.txt_apellidos, self.txt_direccion]
        for field in text_fields:
            if not field.text().strip():
                self.set_status(field, "error")
                errores = True
            else:
                self.set_status(field, "normal")

        combos = [self.cb_especialidad, self.cb_estado]
        for combo in combos:
            if combo.currentIndex() == 0: 
                self.set_status(combo, "error")
                errores = True
            else:
                self.set_status(combo, "normal")

        telefonos = [self.txt_tel1] + self.inputs_extra_telefonos
        for tel in telefonos:
            if not tel.text().strip() or not tel.text().isdigit():
                self.set_status(tel, "error")
                errores = True
            else:
                self.set_status(tel, "normal")

        if errores:
            QMessageBox.warning(self, "Error", "Por favor corrige los campos marcados en rojo.")
            return

        tel2_val = self.inputs_extra_telefonos[0].text() if self.inputs_extra_telefonos else ""
        
        with open(ARCHIVO_DB, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.txt_nombres.text(), self.txt_apellidos.text(), self.cb_especialidad.currentText(),
                self.txt_tel1.text(), tel2_val, self.txt_direccion.text(), self.cb_estado.currentText()
            ])

        self.flash_verde()
        QMessageBox.information(self, "Éxito", "Médico registrado correctamente.")
        
        self.txt_nombres.clear()
        self.txt_apellidos.clear()
        self.txt_tel1.clear()
        for extra in self.inputs_extra_telefonos:
            extra.deleteLater() 
        self.inputs_extra_telefonos.clear()
        self.txt_direccion.clear()
        self.cb_especialidad.setCurrentIndex(0)
        self.cb_estado.setCurrentIndex(0)

# ----------------------------------------------------------------
# CLASE 2: CONSULTAR MÉDICOS (TODO EN UNO: FILTROS + EDICIÓN + ELIMINAR)
# ----------------------------------------------------------------
class WidgetConsultar(QWidget):
    def __init__(self):
        super().__init__()
        self.fila_seleccionada = -1 
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        titulo = QLabel("🟩 Consultar y Gestionar Médicos")
        titulo.setObjectName("titulo_page")
        self.layout.addWidget(titulo)

        # --- A. BARRA DE FILTROS ---
        frame_filtros = QFrame()
        frame_filtros.setObjectName("filtro_container")
        layout_filtros = QHBoxLayout(frame_filtros)
        layout_filtros.setContentsMargins(5, 5, 5, 5)
        
        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Buscar por Nombre o Apellido...")
        self.txt_buscar.setObjectName("input_busqueda")
        self.txt_buscar.textChanged.connect(self.filtrar_tabla)

        self.filtro_esp = QComboBox()
        self.filtro_esp.addItem("Todas las Especialidades")
        self.filtro_esp.addItems(["Medicina General", "Cardiología", "Pediatría", "Dermatología", "Neurología"])
        self.filtro_esp.currentTextChanged.connect(self.filtrar_tabla)

        self.filtro_estado = QComboBox()
        self.filtro_estado.addItem("Todos los Estados")
        self.filtro_estado.addItems(["Activo", "Inactivo", "Vacaciones", "Licencia"])
        self.filtro_estado.currentTextChanged.connect(self.filtrar_tabla)

        btn_refrescar = QPushButton("🔄")
        btn_refrescar.setFixedSize(35, 35)
        btn_refrescar.setObjectName("btnRefrescarSmall")
        btn_refrescar.clicked.connect(self.cargar_datos)

        layout_filtros.addWidget(self.txt_buscar, 2)
        layout_filtros.addWidget(self.filtro_esp, 1)
        layout_filtros.addWidget(self.filtro_estado, 1)
        layout_filtros.addWidget(btn_refrescar)

        self.layout.addWidget(frame_filtros)

        # --- B. TABLA ---
        self.crear_tabla()

        # --- C. FORMULARIO EDICIÓN (OCULTO) ---
        self.crear_formulario_edicion()
        self.frame_edicion.hide()

    def crear_tabla(self):
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(8) # 7 Datos + 1 Acciones
        self.tabla.setHorizontalHeaderLabels(["Nombres", "Apellidos", "Especialidad", "Tel 1", "Tel 2", "Dirección", "Estado", "Acciones"])
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)

        self.layout.addWidget(self.tabla)

    def crear_formulario_edicion(self):
        self.frame_edicion = QFrame()
        self.frame_edicion.setObjectName("frame_edicion")
        layout_form = QVBoxLayout(self.frame_edicion)
        
        lbl_titulo = QLabel("✏️ Editando Médico Seleccionado")
        lbl_titulo.setObjectName("titulo_edicion")
        layout_form.addWidget(lbl_titulo)

        grid = QFormLayout()
        
        self.edit_nombres = QLineEdit()
        self.edit_apellidos = QLineEdit()
        self.edit_esp = QComboBox()
        self.edit_esp.addItems(["Medicina General", "Cardiología", "Pediatría", "Dermatología", "Neurología"])
        
        self.edit_tel1 = QLineEdit()
        self.edit_tel1.textChanged.connect(lambda: self.validar_numeros(self.edit_tel1))
        self.edit_tel2 = QLineEdit()
        self.edit_tel2.textChanged.connect(lambda: self.validar_numeros(self.edit_tel2))
        
        self.edit_dir = QLineEdit()
        self.edit_estado = QComboBox()
        self.edit_estado.addItems(["Activo", "Inactivo", "Vacaciones", "Licencia"])

        grid.addRow("Nombres:", self.edit_nombres)
        grid.addRow("Apellidos:", self.edit_apellidos)
        grid.addRow("Especialidad:", self.edit_esp)
        grid.addRow("Teléfono 1:", self.edit_tel1)
        grid.addRow("Teléfono 2:", self.edit_tel2)
        grid.addRow("Dirección:", self.edit_dir)
        grid.addRow("Estado:", self.edit_estado)

        layout_form.addLayout(grid)

        layout_btns = QHBoxLayout()
        btn_guardar = QPushButton("Guardar Cambios")
        btn_guardar.setObjectName("btnGuardar")
        btn_guardar.clicked.connect(self.guardar_cambios)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnCancelar")
        btn_cancelar.clicked.connect(self.cancelar_edicion)

        layout_btns.addWidget(btn_guardar)
        layout_btns.addWidget(btn_cancelar)
        layout_form.addLayout(layout_btns)

        self.layout.addWidget(self.frame_edicion)

    def showEvent(self, event):
        self.cargar_datos()
        self.cancelar_edicion()
        super().showEvent(event)

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        # Limpiamos filtros visuales al recargar todo
        self.txt_buscar.clear()
        
        if os.path.exists(ARCHIVO_DB):
            with open(ARCHIVO_DB, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                datos = list(reader)
                
                if len(datos) > 1:
                    for i, row_data in enumerate(datos[1:]): 
                        self.tabla.insertRow(i)
                        
                        # Llenar datos (7 columnas)
                        for col, data in enumerate(row_data):
                            if col < 7:
                                self.tabla.setItem(i, col, QTableWidgetItem(str(data)))
                        
                        # Crear botones de acción
                        widget_acciones = QWidget()
                        layout_acciones = QHBoxLayout(widget_acciones)
                        layout_acciones.setContentsMargins(5, 2, 5, 2)
                        
                        btn_editar = QPushButton("✏️")
                        btn_editar.setObjectName("btnTablaEditar")
                        btn_editar.clicked.connect(lambda _, idx=i: self.cargar_formulario(idx))

                        btn_eliminar = QPushButton("🗑️")
                        btn_eliminar.setObjectName("btnTablaEliminar")
                        btn_eliminar.clicked.connect(lambda _, idx=i: self.eliminar_fila(idx))

                        layout_acciones.addWidget(btn_editar)
                        layout_acciones.addWidget(btn_eliminar)
                        
                        self.tabla.setCellWidget(i, 7, widget_acciones)

    def filtrar_tabla(self):
        texto_busqueda = self.txt_buscar.text().lower().strip()
        filtro_esp = self.filtro_esp.currentText()
        filtro_est = self.filtro_estado.currentText()

        for fila in range(self.tabla.rowCount()):
            # --- PROTECCIÓN CONTRA NONE (CELDAS VACÍAS) ---
            item_nom = self.tabla.item(fila, 0)
            item_ape = self.tabla.item(fila, 1)
            item_esp = self.tabla.item(fila, 2)
            item_est = self.tabla.item(fila, 6)
            
            nombre = item_nom.text().lower() if item_nom else ""
            apellido = item_ape.text().lower() if item_ape else ""
            especialidad = item_esp.text() if item_esp else ""
            estado = item_est.text() if item_est else ""

            match_texto = (texto_busqueda in nombre) or (texto_busqueda in apellido)
            match_esp = (filtro_esp == "Todas las Especialidades") or (filtro_esp == especialidad)
            match_est = (filtro_est == "Todos los Estados") or (filtro_est == estado)

            if match_texto and match_esp and match_est:
                self.tabla.setRowHidden(fila, False)
            else:
                self.tabla.setRowHidden(fila, True)

    def cargar_formulario(self, index_fila):
        self.fila_seleccionada = index_fila
        
        # --- PROTECCIÓN CONTRA NONE AL CARGAR DATOS ---
        def get_safe_text(col):
            item = self.tabla.item(index_fila, col)
            return item.text() if item else ""

        self.edit_nombres.setText(get_safe_text(0))
        self.edit_apellidos.setText(get_safe_text(1))
        self.edit_esp.setCurrentText(get_safe_text(2))
        self.edit_tel1.setText(get_safe_text(3))
        self.edit_tel2.setText(get_safe_text(4))
        self.edit_dir.setText(get_safe_text(5))
        self.edit_estado.setCurrentText(get_safe_text(6))

        self.frame_edicion.show()
        # Asegurarnos de que el usuario vea el formulario
        QTimer.singleShot(100, lambda: self.tabla.scrollToBottom())

    def guardar_cambios(self):
        if self.fila_seleccionada == -1: return

        if not self.edit_nombres.text() or not self.edit_tel1.text().isdigit():
            QMessageBox.warning(self, "Error", "Verifica los nombres y que el teléfono sea numérico.")
            return

        filas = []
        with open(ARCHIVO_DB, mode='r', encoding='utf-8') as f:
            filas = list(csv.reader(f))

        idx_csv = self.fila_seleccionada + 1
        if idx_csv < len(filas):
            filas[idx_csv] = [
                self.edit_nombres.text(),
                self.edit_apellidos.text(),
                self.edit_esp.currentText(),
                self.edit_tel1.text(),
                self.edit_tel2.text(),
                self.edit_dir.text(),
                self.edit_estado.currentText()
            ]

            with open(ARCHIVO_DB, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(filas)

            QMessageBox.information(self, "Actualizado", "Datos actualizados correctamente.")
            self.cancelar_edicion()
            self.cargar_datos() # Recarga tabla y restaura filtros

    def eliminar_fila(self, index_fila):
        # PROTECCIÓN: Obtener nombre/apellido seguramente para el mensaje
        item_nom = self.tabla.item(index_fila, 0)
        item_ape = self.tabla.item(index_fila, 1)
        nombre = item_nom.text() if item_nom else "Desconocido"
        apellido = item_ape.text() if item_ape else ""

        resp = QMessageBox.question(self, "Confirmar", f"¿Seguro que deseas eliminar a {nombre} {apellido}?", 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if resp == QMessageBox.StandardButton.Yes:
            filas = []
            with open(ARCHIVO_DB, mode='r', encoding='utf-8') as f:
                filas = list(csv.reader(f))
            
            del filas[index_fila + 1]

            with open(ARCHIVO_DB, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(filas)
            
            self.cargar_datos()
            self.cancelar_edicion() # Si estaba editando ese mismo, cerrar form

    def cancelar_edicion(self):
        self.frame_edicion.hide()
        self.fila_seleccionada = -1
        self.edit_nombres.clear()
        self.edit_apellidos.clear()
        self.edit_tel1.clear()
        self.edit_tel2.clear()
        self.edit_dir.clear()

    def validar_numeros(self, widget):
        texto = widget.text()
        if texto and not texto.isdigit():
            widget.setStyleSheet("border: 2px solid #e74c3c;")
        else:
            widget.setStyleSheet("")

# ----------------------------------------------------------------
# VENTANA PRINCIPAL (AHORA SOLO 2 PESTAÑAS)
# ----------------------------------------------------------------
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Hospitalario Pro v3")
        self.resize(1100, 750) # Un poco más alto para ver el form de edición

        self.cargar_hoja_estilos()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. SIDEBAR
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar_frame")
        self.sidebar.setFixedWidth(200)
        self.layout_sidebar = QVBoxLayout(self.sidebar)
        self.layout_sidebar.setContentsMargins(0, 0, 0, 0)

        self.btn_menu = QPushButton("☰ MENU")
        self.btn_menu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_menu.setStyleSheet("background-color: #16a085; font-weight: bold;")
        self.btn_menu.clicked.connect(self.animar_sidebar)
        self.layout_sidebar.addWidget(self.btn_menu)

        self.botones_nav = []
        # ELIMINADO EL MODULO "ACTUALIZAR" DEL MENÚ
        opciones = [("🟦 Registrar", 0), ("🟩 Consultar", 1)]

        for texto, indice in opciones:
            btn = QPushButton(f" {texto}")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=indice: self.cambiar_pagina(idx))
            self.layout_sidebar.addWidget(btn)
            self.botones_nav.append(btn)
        
        self.layout_sidebar.addStretch()

        # 2. CONTENIDO
        self.contenido_frame = QFrame()
        self.contenido_frame.setObjectName("content_frame")
        self.layout_contenido = QVBoxLayout(self.contenido_frame)

        self.stacked_widget = QStackedWidget()
        
        self.page_registrar = WidgetRegistrar()
        self.page_consultar = WidgetConsultar()

        self.stacked_widget.addWidget(self.page_registrar)
        self.stacked_widget.addWidget(self.page_consultar)

        self.layout_contenido.addWidget(self.stacked_widget)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.contenido_frame)
        
        self.botones_nav[0].click()

    def cargar_hoja_estilos(self):
        try:
            with open(ARCHIVO_ESTILOS, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo {ARCHIVO_ESTILOS}")
        except Exception as e:
            print(f"Error cargando estilos: {e}")

    def cambiar_pagina(self, indice):
        self.stacked_widget.setCurrentIndex(indice)
        for i, btn in enumerate(self.botones_nav):
            btn.setChecked(i == indice)

    def animar_sidebar(self):
        width = self.sidebar.width()
        nuevo_ancho = 60 if width == 200 else 200
        
        if width == 200:
            self.btn_menu.setText("☰")
            for btn in self.botones_nav:
                txt = btn.text().strip()
                btn.setText(txt.split(" ")[0] if " " in txt else txt[0])
        else:
            self.btn_menu.setText("☰ MENU")
            full_txt = ["🟦 Registrar", "🟩 Consultar"]
            for i, btn in enumerate(self.botones_nav):
                btn.setText(f" {full_txt[i]}")

        self.anim = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.anim.setDuration(300)
        self.anim.setStartValue(width)
        self.anim.setEndValue(nuevo_ancho)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.anim.start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
