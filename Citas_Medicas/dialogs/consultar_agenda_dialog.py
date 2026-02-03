from datetime import date

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDateEdit, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout
)

from ..citas_controller import CitasMedicasController


class ConsultarAgendaDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Consultar Agenda")
        self.setModal(True)
        self.setMinimumWidth(750)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("🗓️ Consultar Agenda por Médico")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        form = QFormLayout()

        self.cmb_medico = QComboBox()
        # REEMPLAZO: Cargamos los médicos guardando su ID de forma oculta
        medicos_data = self.controller.obtener_todos_medicos()
        for m in medicos_data:
            # addItem(Texto visible, Dato interno)
            self.cmb_medico.addItem(m["nombre_completo"], m["id"])
            
        form.addRow("Médico:", self.cmb_medico)

        self.date_fecha = QDateEdit()
        self.date_fecha.setCalendarPopup(True)
        self.date_fecha.setDate(date.today())
        form.addRow("Fecha:", self.date_fecha)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_buscar = QPushButton("Consultar")
        btn_buscar.clicked.connect(self._consultar)
        btns.addWidget(btn_buscar)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.reject)
        btns.addWidget(btn_cerrar)
        layout.addLayout(btns)

        self.tabla = QTableWidget(0, 5)
        self.tabla.setHorizontalHeaderLabels(["Hora", "Paciente", "Especialidad", "Estado", "Código"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tabla)

    def _consultar(self):
        id_medico = self.cmb_medico.currentData()
        
        if id_medico is None:
            QMessageBox.warning(self, "Error", "Seleccione un médico válido.")
            return

        qd = self.date_fecha.date()
        fecha = date(qd.year(), qd.month(), qd.day())

        # Ahora enviamos el ID al controlador
        citas = self.controller.consultar_agenda(id_medico, fecha)
        
        self.tabla.setRowCount(0)

        if not citas:
            QMessageBox.information(self, "Agenda", "No existen citas para la fecha seleccionada.")
            return

        for c in citas:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            # Asegúrate de que c.especialidad existe en tu objeto CitaMedica
            vals = [
                str(c.hora),
                c.nombre_paciente,
                c.especialidad,
                c.estado,
                c.codigo
            ]
            for col, v in enumerate(vals):
                self.tabla.setItem(row, col, QTableWidgetItem(str(v)))
