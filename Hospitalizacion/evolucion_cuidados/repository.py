from typing import List, Optional
import sqlite3
from core.database import crear_conexion, inicializar_db
from datetime import datetime


class EvolucionRepository:
    def __init__(self):
        try:
            inicializar_db()
        except Exception:
            pass
        self.conn = crear_conexion()
        self._ensure_table()

    def _ensure_table(self):
        if not self.conn:
            return
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS evoluciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_dni TEXT,
                nota TEXT,
                fecha TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cuidados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_dni TEXT,
                datos TEXT,
                fecha TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def registrar_evolucion(self, paciente_dni: str, nota: str) -> bool:
        if not self.conn:
            return False
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO evoluciones (paciente_dni, nota, fecha) VALUES (?,?,?)",
                        (paciente_dni, nota, datetime.now().isoformat()))
            self.conn.commit()
            return True
        except Exception:
            return False

    def listar_por_paciente(self, paciente_dni: str) -> List[dict]:
        if not self.conn:
            return []
        cur = self.conn.cursor()
        rows = cur.execute("SELECT id, paciente_dni, nota, fecha FROM evoluciones WHERE paciente_dni=? ORDER BY fecha DESC", (paciente_dni,)).fetchall()
        return [{"id": r[0], "paciente_dni": r[1], "nota": r[2], "fecha": r[3]} for r in rows]


repo_evolucion = EvolucionRepository()
