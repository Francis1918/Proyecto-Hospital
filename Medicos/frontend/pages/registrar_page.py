# Medicos/frontend/pages/registrar_page.py

import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QPushButton, QFrame, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from Medicos.backend.logic_medicos import LogicaMedicos 
import core.theme as theme
import core.utils as utils

class WidgetRegistrar(QWidget):
    medico_guardado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.logic = LogicaMedicos()
        self.input_tel2 = None     # Referencia al campo extra
        self.widget_tel2 = None    # Referencia al contenedor extra

        # --- LAYOUT PRINCIPAL CON SCROLL ---
        layout_main = QVBoxLayout(self)
        layout_main.setContentsMargins(0,0,0,0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;") 

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(30) 
        self.content_layout.setContentsMargins(30, 30, 30, 30)

        # ---------------------------------------------
        # 1. SECCIÓN: INFORMACIÓN PERSONAL
        # ---------------------------------------------
        
        # --- A) CÉDULA (NUEVO CAMPO) ---
        self.txt_cedula = self.crear_campo_input("Ej. 1712345678")
        # Conectamos validación de números (rojo si letras o length > 10)
        self.txt_cedula.textChanged.connect(lambda: self.validar_numeros_visual(self.txt_cedula))

        # --- B) NOMBRES Y APELLIDOS ---
        row_nombres = QHBoxLayout()
        row_nombres.setSpacing(20)
        
        self.txt_nombres = self.crear_campo_input("Nombres")
        # Conectamos validación de texto (rojo si números o símbolos)
        self.txt_nombres.textChanged.connect(lambda: self.validar_texto_visual(self.txt_nombres))
        
        self.txt_apellidos = self.crear_campo_input("Apellidos")
        # Conectamos validación de texto
        self.txt_apellidos.textChanged.connect(lambda: self.validar_texto_visual(self.txt_apellidos))
        
        row_nombres.addWidget(self.crear_grupo_input("Nombre(s)", self.txt_nombres))
        row_nombres.addWidget(self.crear_grupo_input("Apellido(s)", self.txt_apellidos))

        # --- C) ESPECIALIDAD Y ESTADO ---
        row_profesional = QHBoxLayout()
        row_profesional.setSpacing(20)

        self.cb_especialidad = QComboBox()
        self.cb_especialidad.setStyleSheet(theme.STYLES["combobox"])
        self.cb_especialidad.addItems(["Seleccione", "Medicina General", "Cardiología", "Pediatría", "Dermatología", "Neurología"])

        self.cb_estado = QComboBox()
        self.cb_estado.setStyleSheet(theme.STYLES["combobox"])
        self.cb_estado.addItems(["Seleccione", "Activo", "Inactivo", "Vacaciones", "Licencia"])

        row_profesional.addWidget(self.crear_grupo_input("Especialidad", self.cb_especialidad))
        row_profesional.addWidget(self.crear_grupo_input("Estado Actual", self.cb_estado))

        # --- ARMADO VISUAL SECCIÓN 1 ---
        layout_personal = QVBoxLayout()
        layout_personal.addWidget(self.crear_grupo_input("Cédula / DNI", self.txt_cedula)) # La cédula va primero
        layout_personal.addSpacing(10)
        layout_personal.addLayout(row_nombres)
        layout_personal.addSpacing(10)
        layout_personal.addLayout(row_profesional)

        self.content_layout.addWidget(self.crear_seccion(
            "Perfil del Médico", 
            "Identificación e información profesional.", 
            layout_personal
        ))

        # ---------------------------------------------
        # 2. SECCIÓN: CONTACTO Y UBICACIÓN
        # ---------------------------------------------
        layout_contacto = QVBoxLayout()
        
        # Dirección
        self.txt_direccion = self.crear_campo_input("Dirección domiciliaria")
        layout_contacto.addWidget(self.crear_grupo_input("Dirección", self.txt_direccion))
        
        layout_contacto.addSpacing(15)

        # Teléfonos
        lbl_tel = QLabel("Teléfono(s)")
        lbl_tel.setStyleSheet(f"border: none; color: {theme.AppPalette.black_02}; font-weight: 600;")
        layout_contacto.addWidget(lbl_tel)

        self.container_telefonos = QVBoxLayout()
        self.container_telefonos.setSpacing(10)

        # Teléfono 1 (Obligatorio)
        self.txt_tel1 = self.crear_campo_input("Teléfono Principal (Solo números)")
        self.txt_tel1.textChanged.connect(lambda: self.validar_numeros_visual(self.txt_tel1))
        self.container_telefonos.addWidget(self.txt_tel1)

        layout_contacto.addLayout(self.container_telefonos)

        # Botón agregar teléfono
        self.btn_add_tel = QPushButton(" Agregar otro teléfono")
        self.btn_add_tel.setIcon(utils.get_icon("plus.svg", color=theme.AppPalette.Primary))
        self.btn_add_tel.setStyleSheet(f"""
            QPushButton {{ color: {theme.AppPalette.Primary}; border: none; text-align: left; font-weight: bold; background: transparent; }}
            QPushButton:hover {{ text-decoration: underline; }}
        """)
        self.btn_add_tel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_tel.clicked.connect(self.agregar_telefono_extra)
        
        layout_contacto.addWidget(self.btn_add_tel)

        self.content_layout.addWidget(self.crear_seccion(
            "Contacto", 
            "Métodos para contactar al especialista.", 
            layout_contacto
        ))

        self.content_layout.addStretch() 

        # ---------------------------------------------
        # BOTÓN GUARDAR
        # ---------------------------------------------
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_guardar = QPushButton(" Guardar Médico")
        btn_guardar.setIcon(utils.get_icon("save.svg", color="white"))
        btn_guardar.setStyleSheet(theme.STYLES["btn_primary"])
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.setFixedWidth(200)
        btn_guardar.clicked.connect(self.guardar_datos)
        
        btn_layout.addWidget(btn_guardar)
        
        self.content_layout.addLayout(btn_layout)
        
        scroll.setWidget(self.content_widget)
        layout_main.addWidget(scroll)

    # ==========================================
    # MÉTODOS DE DISEÑO (HELPERS)
    # ==========================================
    def crear_seccion(self, titulo, subtitulo, layout_contenido):
        """Crea una tarjeta visual estilo 'Settings'."""
        card = QFrame()
        card.setStyleSheet(theme.STYLES["card"])
        
        l_card = QVBoxLayout(card)
        l_card.setContentsMargins(20, 20, 20, 20)
        l_card.setSpacing(15)

        # Cabecera de la sección
        lbl_main = QLabel(titulo)
        lbl_main.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {theme.AppPalette.black_01}; border: none;")
        
        lbl_sub = QLabel(subtitulo)
        lbl_sub.setStyleSheet(f"font-size: 12px; color: {theme.AppPalette.black_01}; margin-bottom: 5px; border: none;")

        # Línea separadora suave
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet(f"border: none; background-color: {theme.AppPalette.Border}; max-height: 1px;")

        l_card.addWidget(lbl_main)
        l_card.addWidget(lbl_sub)
        l_card.addWidget(line)
        l_card.addLayout(layout_contenido)
        
        return card

    def crear_grupo_input(self, label_text, widget):
        """Crea un layout vertical: Label arriba, Input abajo."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(5)
        
        lbl = QLabel(label_text)
        lbl.setStyleSheet(f"font-weight: 600; color: {theme.AppPalette.black_02}; border: none;")
        
        layout.addWidget(lbl)
        layout.addWidget(widget)
        return container

    def crear_campo_input(self, placeholder):
        txt = QLineEdit()
        txt.setPlaceholderText(placeholder)
        return txt

    # ==========================================
    # LÓGICA DE TELÉFONOS (AGREGAR / QUITAR)
    # ==========================================
    def agregar_telefono_extra(self):
        # Limitamos a máximo 2 teléfonos (1 principal + 1 extra)
        if self.widget_tel2 is not None:
            QMessageBox.information(self, "Aviso", "Solo se permiten 2 números de contacto por ahora.")
            return

        # Creamos un contenedor horizontal para [Input] [Botón Eliminar]
        self.widget_tel2 = QWidget()
        layout_row = QHBoxLayout(self.widget_tel2)
        layout_row.setContentsMargins(0,0,0,0)
        layout_row.setSpacing(10)

        # Input
        self.input_tel2 = self.crear_campo_input("Teléfono Secundario (Opcional)")
        self.input_tel2.textChanged.connect(lambda: self.validar_numeros_visual(self.input_tel2))
        
        # Botón Eliminar (Icono Trash)
        btn_del = QPushButton()
        btn_del.setIcon(utils.get_icon("trash.svg", color=theme.AppPalette.Danger))
        btn_del.setFixedSize(36, 36)
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        # Estilo rojo suave para el botón de borrar
        btn_del.setStyleSheet(f"""
            QPushButton {{ 
                background-color: #FFF5F5; 
                border: 1px solid {theme.AppPalette.Danger}; 
                border-radius: 6px; 
            }}
            QPushButton:hover {{ background-color: #FFA5A5; }}
        """)
        
        btn_del.clicked.connect(self.eliminar_telefono_extra)

        layout_row.addWidget(self.input_tel2)
        layout_row.addWidget(btn_del)

        self.container_telefonos.addWidget(self.widget_tel2)

    def eliminar_telefono_extra(self):
        if self.widget_tel2:
            self.widget_tel2.deleteLater()
            self.widget_tel2 = None
            self.input_tel2 = None

    def validar_numeros_visual(self, widget):
        texto = widget.text()
        es_invalido = (texto and not texto.isdigit()) or len(texto) > 10

        if es_invalido:
            # Borde Rojo y texto rojo
            widget.setStyleSheet(f"border: 1px solid {theme.AppPalette.Danger}; color: {theme.AppPalette.Danger};")

            if len(texto) > 10:
                widget.setToolTip("Máximo 10 dígitos permitidos")
            else:
                widget.setToolTip("Solo se permiten números")
        else:
            # Estilo original (limpio)
            widget.setStyleSheet(theme.STYLES["combobox"].replace("QComboBox", "QLineEdit"))
            widget.setToolTip("")

    # ==========================================
    # GUARDADO Y LIMPIEZA
    # ==========================================
    def guardar_datos(self):
        # Obtenemos valor del tel 2 si existe
        tel2_val = ""
        if self.input_tel2:
            tel2_val = self.input_tel2.text()

        exito, msg = self.logic.crear_medico(
            self.txt_cedula.text().strip(),  # <--- NUEVO
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
            QMessageBox.warning(self, "Atención", msg)

    def limpiar_formulario(self):
        self.txt_cedula.clear()
        self.txt_nombres.clear()
        self.txt_apellidos.clear()
        self.txt_tel1.clear()
        self.txt_direccion.clear()
        self.cb_especialidad.setCurrentIndex(0)
        self.cb_estado.setCurrentIndex(0)

        self.eliminar_telefono_extra()

    def validar_texto_visual(self, widget):
        texto = widget.text()
        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*$'
        
        if not re.match(patron, texto):
            # Si NO coincide (tiene números o símbolos) -> Rojo
            widget.setStyleSheet(f"border: 1px solid {theme.AppPalette.Danger}; color: {theme.AppPalette.Danger};")
            widget.setToolTip("Solo se permiten letras y espacios")
        else:
            # Si coincide -> Normal
            widget.setStyleSheet(theme.STYLES["combobox"].replace("QComboBox", "QLineEdit"))
            widget.setToolTip("")
    
