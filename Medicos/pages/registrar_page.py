from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QPushButton, QFrame, QFormLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from logic_medicos import LogicaMedicos 
import theme
import utils

class WidgetRegistrar(QWidget):
    medico_guardado = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Instanciamos la lógica
        self.logic = LogicaMedicos()
        
        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)
        self.inputs_extra_telefonos = [] 

        lbl_titulo = QLabel("Registrar Nuevo Médico")
        lbl_titulo.setObjectName("h1") 
        self.layout_principal.addWidget(lbl_titulo)

        card = QFrame()
        card.setStyleSheet(theme.STYLES["card"])
        
        layout_form = QFormLayout(card)
        layout_form.setSpacing(15)
        layout_form.setContentsMargins(30, 30, 30, 30)

        self.txt_nombres = QLineEdit()
        self.txt_apellidos = QLineEdit()
        
        self.cb_especialidad = QComboBox()
        self.cb_especialidad.setStyleSheet(theme.STYLES["combobox"])
        # "Seleccione" ahora será detectado como error por la lógica
        self.cb_especialidad.addItems(["Seleccione", "Medicina General", "Cardiología", "Pediatría", "Dermatología", "Neurología"])
        
        self.container_telefonos = QWidget()
        self.layout_telefonos = QVBoxLayout(self.container_telefonos)
        self.layout_telefonos.setContentsMargins(0,0,0,0)
        
        # Validación Visual (UX): Mantiene el borde rojo mientras escribes
        self.txt_tel1 = self.crear_input_telefono() 
        self.layout_telefonos.addWidget(self.txt_tel1)

        self.btn_add_tel = QPushButton(" Agregar otro teléfono")
        self.btn_add_tel.setIcon(utils.get_icon("plus.svg", color=theme.Palette.Primary))
        self.btn_add_tel.setStyleSheet(f"color: {theme.Palette.Primary}; border: none; text-align: left; font-weight: bold;")
        self.btn_add_tel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_tel.clicked.connect(self.agregar_telefono_extra)
        self.layout_telefonos.addWidget(self.btn_add_tel)

        self.txt_direccion = QLineEdit()
        self.cb_estado = QComboBox()
        self.cb_estado.setStyleSheet(theme.STYLES["combobox"])
        self.cb_estado.addItems(["Seleccione", "Activo", "Inactivo", "Vacaciones", "Licencia"])

        def label(text):
            l = QLabel(text)
            l.setStyleSheet(f"font-weight: bold; color: {theme.Palette.Text_Primary};")
            return l

        layout_form.addRow(label("Nombres:"), self.txt_nombres)
        layout_form.addRow(label("Apellidos:"), self.txt_apellidos)
        layout_form.addRow(label("Especialidad:"), self.cb_especialidad)
        layout_form.addRow(label("Teléfono(s):"), self.container_telefonos)
        layout_form.addRow(label("Dirección:"), self.txt_direccion)
        layout_form.addRow(label("Estado:"), self.cb_estado)

        self.layout_principal.addWidget(card)

        btn_guardar = QPushButton(" Guardar Médico")
        btn_guardar.setIcon(utils.get_icon("save.svg", color="white"))
        btn_guardar.setIconSize(QSize(20, 20))
        btn_guardar.setStyleSheet(theme.STYLES["btn_primary"])
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.clicked.connect(self.guardar_datos)
        
        container_btn = QHBoxLayout()
        container_btn.addStretch()
        container_btn.addWidget(btn_guardar)
        self.layout_principal.addLayout(container_btn)
        self.layout_principal.addStretch()

    def crear_input_telefono(self):
        txt = QLineEdit()
        txt.setPlaceholderText("Solo números...")
        # Mantenemos la validación visual para buena experiencia de usuario
        txt.textChanged.connect(lambda: self.validar_numeros_visual(txt))
        return txt

    def validar_numeros_visual(self, widget):
        texto = widget.text()
        if texto and not texto.isdigit():
            widget.setStyleSheet(f"border: 1px solid {theme.Palette.Danger}; color: {theme.Palette.Danger};")
        else:
            widget.setStyleSheet("") # Restaura estilo por defecto

    def agregar_telefono_extra(self):
        if len(self.inputs_extra_telefonos) < 1: 
            nuevo_tel = self.crear_input_telefono()
            self.inputs_extra_telefonos.append(nuevo_tel)
            self.layout_telefonos.insertWidget(self.layout_telefonos.count()-1, nuevo_tel)
        else:
            QMessageBox.information(self, "Aviso", "Máximo 2 teléfonos permitidos.")

    def guardar_datos(self):
        # Recopilar datos
        tel2_val = self.inputs_extra_telefonos[0].text() if self.inputs_extra_telefonos else ""
        
        # --- AQUI ESTA EL CAMBIO: LLAMAMOS A LA LOGICA ---
        exito, msg = self.logic.crear_medico(
            self.txt_nombres.text().strip(),
            self.txt_apellidos.text().strip(),
            self.cb_especialidad.currentText(),
            self.txt_tel1.text().strip(),
            tel2_val.strip(),
            self.txt_direccion.text().strip(),
            self.cb_estado.currentText()
        )

        if exito:
            QMessageBox.information(self, "Éxito", msg)
            self.medico_guardado.emit()
            self.limpiar_formulario()
        else:
            # Si falla (ej. puso letras en el telefono o dejó Seleccione), sale el error
            QMessageBox.warning(self, "Atención", msg)

    def limpiar_formulario(self):
        self.txt_nombres.clear()
        self.txt_apellidos.clear()
        self.txt_tel1.clear()
        self.txt_direccion.clear()
        self.cb_especialidad.setCurrentIndex(0)
        self.cb_estado.setCurrentIndex(0)
        for t in self.inputs_extra_telefonos: 
            t.deleteLater()
        self.inputs_extra_telefonos.clear()