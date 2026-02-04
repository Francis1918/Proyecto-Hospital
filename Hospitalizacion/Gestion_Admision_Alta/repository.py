from typing import Optional
from core.database import crear_conexion, inicializar_db
from datetime import datetime


class AdmisionRepository:
    def __init__(self):
        try:
            inicializar_db()
        except Exception:
            pass
        self.conn = crear_conexion()
        self._ensure_tables()

    def _ensure_tables(self):
        # The core DB already contains pacientes and hospitalizaciones; we ensure minimal data is available
        if not self.conn:
            return
        cur = self.conn.cursor()
        # Areas table (simple inventory of capacities)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS areas_hospital (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE,
                capacidad INTEGER DEFAULT 0,
                ocupadas INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def get_paciente_por_cedula(self, cedula: str) -> Optional[dict]:
        if not self.conn:
            return None
        cur = self.conn.cursor()
        row = cur.execute("SELECT id, dni, nombres, apellidos FROM pacientes WHERE dni=?", (cedula,)).fetchone()
        if not row:
            return None
        return {"id": row[0], "dni": row[1], "nombres": row[2], "apellidos": row[3]}

    def esta_hospitalizado(self, cedula: str) -> bool:
        paciente = self.get_paciente_por_cedula(cedula)
        if not paciente:
            return False
        cur = self.conn.cursor()
        row = cur.execute("SELECT COUNT(1) FROM hospitalizaciones WHERE paciente_id=?", (paciente["id"],)).fetchone()
        return bool(row and row[0] > 0)

    def registrar_ingreso(self, cedula: str, motivo: str, area: str) -> str:
        paciente = self.get_paciente_por_cedula(cedula)
        if not paciente:
            return "Paciente no registrado"
        # comprobar disponibilidad area
        cur = self.conn.cursor()
        row = cur.execute("SELECT id, capacidad, ocupadas FROM areas_hospital WHERE nombre=?", (area,)).fetchone()
        if not row:
            return "Área desconocida"
        _, capacidad, ocupadas = row
        if capacidad - ocupadas <= 0:
            return "No hay camas disponibles en esta área"
        try:
            # insertar hospitalizacion
            cur.execute("INSERT INTO hospitalizaciones (paciente_id, sala_id, fecha_ingreso, estado_paciente) VALUES (?,?,?,?)",
                        (paciente["id"], None, datetime.now().isoformat(), "hospitalizado"))
            # incrementar ocupadas
            cur.execute("UPDATE areas_hospital SET ocupadas = ocupadas + 1 WHERE nombre=?", (area,))
            self.conn.commit()
            return "Ingreso registrado con éxito"
        except Exception:
            return "Error al registrar ingreso"

    def registrar_alta(self, cedula: str, motivo_alta: str) -> str:
        paciente = self.get_paciente_por_cedula(cedula)
        if not paciente:
            return "Paciente no registrado"
        cur = self.conn.cursor()
        row = cur.execute("SELECT id FROM hospitalizaciones WHERE paciente_id=? ORDER BY fecha_ingreso DESC", (paciente["id"],)).fetchone()
        if not row:
            return "El paciente no tiene una hospitalización activa"
        try:
            hid = row[0]
            cur.execute("DELETE FROM hospitalizaciones WHERE id=?", (hid,))
            # Nota: no sabemos el área exacta; no decrementamos ocupadas automáticamente
            self.conn.commit()
            return "Alta registrada con éxito"
        except Exception:
            return "Error al registrar alta"


repo_admision = AdmisionRepository()
