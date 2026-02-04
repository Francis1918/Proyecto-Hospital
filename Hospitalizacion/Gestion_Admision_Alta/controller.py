from .repository import repo_admision
import re


class HospitalController:
    def __init__(self):
        # Delegate storage and queries to repo_admision (DB-backed)
        self.repo = repo_admision

    def validar_cedula(self, cedula):
        if len(cedula) == 10 and cedula.isdigit():
            return True
        return False

    def verificar_disponibilidad(self, area):
        # Try to get area availability from repo
        try:
            cur = self.repo.conn.cursor()
            row = cur.execute("SELECT capacidad, ocupadas FROM areas_hospital WHERE nombre=?", (area,)).fetchone()
            if not row:
                return 0
            capacidad, ocupadas = row
            return max(0, capacidad - ocupadas)
        except Exception:
            return 0

    def registrar_ingreso(self, cedula, motivo, area):
        if not self.validar_cedula(cedula):
            return "Formato de cédula incorrecto"
        return self.repo.registrar_ingreso(cedula, motivo, area)

    def registrar_alta(self, cedula, motivo_alta):
        return self.repo.registrar_alta(cedula, motivo_alta)