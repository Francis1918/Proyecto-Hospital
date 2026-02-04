import sqlite3
from datetime import datetime
from core.database import crear_conexion, inicializar_db
from typing import List, Dict


class VisitasRepository:
    def __init__(self):
        try:
            inicializar_db()
        except Exception:
            pass
        self.conn = crear_conexion()
        self._ensure_tables()

    def _ensure_tables(self):
        if not self.conn:
            return
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visitantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula TEXT UNIQUE,
                nombre TEXT,
                apellidos TEXT,
                restriccion INTEGER DEFAULT 0
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS permisos_visita (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula_paciente TEXT,
                cedula_visitante TEXT,
                fecha TEXT,
                hora TEXT
            )
        """)
        self.conn.commit()

    def registrar_visitante(self, cedula: str, nombre: str, apellidos: str, restriccion: bool=False) -> bool:
        if not self.conn:
            return False
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT OR IGNORE INTO visitantes (cedula, nombre, apellidos, restriccion) VALUES (?,?,?,?)",
                        (cedula, nombre, apellidos, 1 if restriccion else 0))
            self.conn.commit()
            return True
        except Exception:
            return False

    def obtener_visitante(self, cedula: str) -> Dict | None:
        if not self.conn:
            return None
        cur = self.conn.cursor()
        row = cur.execute("SELECT cedula, nombre, apellidos, restriccion FROM visitantes WHERE cedula=?", (cedula,)).fetchone()
        if not row:
            return None
        return {"cedula": row[0], "nombre": row[1], "apellidos": row[2], "restriccion": bool(row[3])}

    def registrar_permiso(self, cedula_paciente: str, cedula_visitante: str) -> bool:
        if not self.conn:
            return False
        try:
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora = datetime.now().strftime("%H:%M:%S")
            cur = self.conn.cursor()
            cur.execute("INSERT INTO permisos_visita (cedula_paciente, cedula_visitante, fecha, hora) VALUES (?,?,?,?)",
                        (cedula_paciente, cedula_visitante, fecha, hora))
            self.conn.commit()
            return True
        except Exception:
            return False

    def listar_permisos(self) -> List[Dict]:
        if not self.conn:
            return []
        cur = self.conn.cursor()
        rows = cur.execute("SELECT cedula_paciente, cedula_visitante, fecha, hora FROM permisos_visita ORDER BY fecha DESC").fetchall()
        return [{"cedula_paciente": r[0], "cedula_visitante": r[1], "fecha": r[2], "hora": r[3]} for r in rows]


repo_visitas = VisitasRepository()
