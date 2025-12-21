from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

VALID_USER = "admin"
VALID_PASS = "admin"

class LoginDialog(QDialog):
    """Login simple para roles JEFE y MEDICO."""
    def __init__(self, rol: str, parent=None):
        super().__init__(parent)
        self.rol = rol
        self.accepted_login = False
        self.setWindowTitle(f"Inicio de sesión ({rol})")
        self.setModal(True)
        self.setMinimumWidth(360)
        layout = QFormLayout(self)
        self.lbl = QLabel(f"Ingrese credenciales para {rol}")
        layout.addRow(self.lbl)
        self.user = QLineEdit()
        self.user.setPlaceholderText("Usuario")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Contraseña")
        layout.addRow("Usuario", self.user)
        layout.addRow("Contraseña", self.password)
        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Ingresar")
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_ok.clicked.connect(self.try_login)
        self.btn_cancel.clicked.connect(self.reject)
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addRow(btns)

    def try_login(self):
        if self.user.text() == VALID_USER and self.password.text() == VALID_PASS:
            self.accepted_login = True
            self.accept()
        else:
            self.lbl.setText("Credenciales incorrectas")
            self.lbl.setStyleSheet("color: #c53030;")


def require_login(rol: str, parent=None) -> bool:
    dlg = LoginDialog(rol, parent)
    result = dlg.exec()
    return dlg.accepted_login and result == QDialog.DialogCode.Accepted
