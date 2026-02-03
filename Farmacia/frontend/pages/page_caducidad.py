from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, 
    QLabel, QHBoxLayout, QComboBox, QPushButton
)
from Farmacia.backend.logic_farmacia import LogicaFarmacia
from PyQt6.QtGui import QColor

class WidgetCaducidad(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = LogicaFarmacia()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        hbox = QHBoxLayout()
        self.combo_filtro = QComboBox()
        self.combo_filtro.addItems(["Próximos a Vencer (30 días)", "Ya Vencidos", "Todos"])
        btn_load = QPushButton("Consultar")
        btn_load.clicked.connect(self.cargar_datos)
        
        hbox.addWidget(QLabel("Filtrar por:"))
        hbox.addWidget(self.combo_filtro)
        hbox.addWidget(btn_load)
        layout.addLayout(hbox)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Producto", "Tipo", "Fecha Caducidad", "Días Restantes"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        map_filtro = {
            "Próximos a Vencer (30 días)": "proximos",
            "Ya Vencidos": "vencidos",
            "Todos": "todos"
        }
        filtro_txt = self.combo_filtro.currentText()
        filtro_val = map_filtro.get(filtro_txt, "proximos")
        
        datos = self.logic.consultar_caducidad(filtro_val)
        self.table.setRowCount(len(datos))
        
        for i, item in enumerate(datos):
            self.table.setItem(i, 0, QTableWidgetItem(item['nombre']))
            self.table.setItem(i, 1, QTableWidgetItem(item['tipo']))
            self.table.setItem(i, 2, QTableWidgetItem(item['fecha']))
            
            dias_item = QTableWidgetItem(str(item['dias']))
            if item['dias'] < 0:
                dias_item.setBackground(QColor("#fed7d7")) # Rojo suave
            elif item['dias'] <= 30:
                dias_item.setBackground(QColor("#fefcbf")) # Amarillo suave
                
            self.table.setItem(i, 3, dias_item)
