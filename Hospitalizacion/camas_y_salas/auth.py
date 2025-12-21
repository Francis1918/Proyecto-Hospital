from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

CREDENTIALS = {
    "JEFE": ("jefe", "jefe"),
    "MEDICO": ("medico", "medico"),
    # Compatibilidad: admin/admin actúa como JEFE
    "ADMIN": ("admin", "admin"),
}

class LoginDialog(QDialog):
    """Login simple que devuelve el rol (JEFE/MEDICO) si es válido."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_role = None
        self.setWindowTitle("Inicio de sesión")
        self.setModal(True)
        self.setMinimumWidth(360)
        layout = QFormLayout(self)
        self.lbl = QLabel("Ingrese usuario y contraseña")
        layout.addRow(self.lbl)
        self.user = QLineEdit()
        self.user.setPlaceholderText("Usuario (jefe/medico)")
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
        u = (self.user.text() or "").strip().lower()
        p = (self.password.text() or "").strip()
        if (u, p) == CREDENTIALS["JEFE"]:
            self.selected_role = "JEFE"
            self.accept()
        elif (u, p) == CREDENTIALS["MEDICO"]:
            self.selected_role = "MEDICO"
            self.accept()
        elif (u, p) == CREDENTIALS["ADMIN"]:
            self.selected_role = "JEFE"
            self.accept()
        else:
            self.lbl.setText("Credenciales incorrectas")
            self.lbl.setStyleSheet("color: #c53030;")


def authenticate_role(parent=None) -> str | None:
    """Abre login y retorna el rol ('JEFE'|'MEDICO') si es válido, o None."""
    dlg = LoginDialog(parent)
    result = dlg.exec()
    return dlg.selected_role if result == QDialog.DialogCode.Accepted else None

def require_login(rol: str, parent=None) -> bool:
    """Compatibilidad: exige que el rol autenticado coincida con 'rol'."""
    r = authenticate_role(parent)
    return r == rol
