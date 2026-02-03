from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout
)

from ..citas_controller import CitasMedicasController


class ConsultarCitaDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Consultar Cita Médica")
        self.setModal(True)
        self.setMinimumWidth(720)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("🔎 Consultar Cita")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        form = QFormLayout()
        self.edt_codigo = QLineEdit()
        self.edt_codigo.setPlaceholderText("Ej: CM-ABC123")
        form.addRow("Código de cita:", self.edt_codigo)

        self.edt_cc = QLineEdit()
        self.edt_cc.setPlaceholderText("(Opcional) Cédula del paciente")
        form.addRow("Cédula:", self.edt_cc)
        layout.addLayout(form)

        btns_busqueda = QHBoxLayout()
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self._buscar)
        btns_busqueda.addWidget(btn_buscar)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.reject)
        btns_busqueda.addWidget(btn_cerrar)
        layout.addLayout(btns_busqueda)

        # Tabla de resultados
        self.tabla = QTableWidget(0, 7)
        self.tabla.setHorizontalHeaderLabels(
            ["Código", "Paciente", "Especialidad", "Médico", "Fecha", "Hora", "Estado"]
        )
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Selecciona fila completa
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tabla)

        # SECCIÓN DE INTEGRACIÓN: Botones de acción sobre la cita seleccionada
        layout.addWidget(QLabel("<b>Acciones sobre la cita seleccionada:</b>"))
        btns_acciones = QHBoxLayout()

        self.btn_modificar = QPushButton("✏️ Modificar Cita")
        self.btn_modificar.clicked.connect(self._on_modificar_click)
        
        self.btn_eliminar = QPushButton("🗑️ Cancelar Cita")
        self.btn_eliminar.clicked.connect(self._on_eliminar_click)
        
        self.btn_estado = QPushButton("🏷️ Registrar Asistencia")
        self.btn_estado.clicked.connect(self._on_estado_click)

        btns_acciones.addWidget(self.btn_modificar)
        btns_acciones.addWidget(self.btn_eliminar)
        btns_acciones.addWidget(self.btn_estado)
        layout.addLayout(btns_acciones)

    def _buscar(self):
        codigo = (self.edt_codigo.text() or "").strip()
        cc = (self.edt_cc.text() or "").strip()

        citas = []
        # Prioridad de búsqueda: Código > Cédula
        if codigo:
            c = self.controller.consultar_cita_por_codigo(codigo)
            if c: citas = [c]
        elif cc:
            ok, msg = self.controller.validar_formato_cedula(cc)
            if not ok:
                QMessageBox.warning(self, "Cédula inválida", msg)
                return
            citas = self.controller.consultar_citas_por_paciente(cc)
        else:
            QMessageBox.information(self, "Buscar", "Ingrese un código o una cédula.")
            return

        self.tabla.setRowCount(0)
        if not citas:
            QMessageBox.information(self, "Sin resultados", "No se encontraron registros.")
            return

        for c in citas:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            # Formateamos valores para la vista (Fecha en DD/MM/AAAA)
            vals = [
                c.codigo, c.nombre_paciente, c.especialidad, 
                c.medico, c.fecha.strftime("%d/%m/%Y"), 
                c.hora.strftime("%H:%M"), c.estado
            ]
            
            for col, v in enumerate(vals):
                item = QTableWidgetItem(str(v))
                
                # Resaltar el estado con color (Integración visual)
                if col == 6: 
                    self._aplicar_color_estado(item, c.estado)
                
                self.tabla.setItem(row, col, item)

    def _aplicar_color_estado(self, item, estado):
        """Asigna colores oportunos según el estado de la cita."""
        colores = {
            "Programada": Qt.GlobalColor.blue,
            "Confirmada": Qt.GlobalColor.blue, # <-- Agregar este
            "Cancelada": Qt.GlobalColor.red,
            "Asistió": Qt.GlobalColor.darkGreen,
            "Reprogramada": Qt.GlobalColor.magenta, # <-- Agregar este
            "Tardanza": Qt.GlobalColor.darkYellow
        }
        if estado in colores:
            item.setForeground(colores[estado])

    def _obtener_codigo_seleccionado(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Selección", "Debe seleccionar una cita de la tabla.")
            return None
        return self.tabla.item(fila, 0).text()

    def _on_modificar_click(self):
        codigo = self._obtener_codigo_seleccionado()
        if codigo:
            from .modificar_cita_dialog import ModificarCitaDialog
            dlg = ModificarCitaDialog(self.controller, self)
            dlg.edt_codigo.setText(codigo)
            dlg._cargar() # Sincroniza datos con la DB
            if dlg.exec(): self._buscar()

    def _on_eliminar_click(self):
        codigo = self._obtener_codigo_seleccionado()
        if codigo:
            from .eliminar_cita_dialog import EliminarCitaDialog
            dlg = EliminarCitaDialog(self.controller, self)
            dlg.edt_codigo.setText(codigo)
            dlg._cargar()
            if dlg.exec(): self._buscar()

    def _on_estado_click(self):
        codigo = self._obtener_codigo_seleccionado()
        if codigo:
            from .registrar_estado_dialog import RegistrarEstadoDialog
            dlg = RegistrarEstadoDialog(self.controller, self)
            dlg.edt_codigo.setText(codigo)
            dlg._cargar()
            if dlg.exec(): self._buscar()