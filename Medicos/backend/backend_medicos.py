# Medicos/backend/backend_medicos.py

import sqlite3
import os

class GestorMedicos:
    def __init__(self):
        # 1. CAMBIO IMPORTANTE: Apuntamos a la base de datos central
        # Usamos ruta relativa para asegurar que encuentre el archivo en la raíz del proyecto
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.db_name = os.path.join(base_dir, "hospital.db")
        
        # Opcional: Ya no llamamos a inicializar_db() aquí forzosamente
        # porque main.py llama a database.py -> inicializar_db() al arrancar.

    def conectar(self):
        """Establece conexión con la base de datos central."""
        return sqlite3.connect(self.db_name)

    # El método inicializar_db se puede conservar como seguridad, 
    # pero database.py es quien manda ahora.

    def registrar_medico(self, nombres, apellidos, especialidad, tel1, tel2, direccion, estado):
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            # Nota: database.py define 'telefono1' y 'telefono2', asegúrate de usar esos nombres
            cursor.execute('''
                INSERT INTO medicos (nombres, apellidos, especialidad, telefono1, telefono2, direccion, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nombres, apellidos, especialidad, tel1, tel2, direccion, estado))
            conn.commit()
            return True, "Médico registrado correctamente."
        except sqlite3.Error as e:
            return False, f"Error al guardar en BD: {e}"
        finally:
            conn.close()

    def obtener_medicos(self, buscar="", filtro_esp="Todas las Especialidades", filtro_est="Todos los Estados"):
        conn = self.conectar()
        cursor = conn.cursor()
        
        query = "SELECT * FROM medicos WHERE 1=1"
        params = []

        if buscar:
            query += " AND (lower(nombres) LIKE ? OR lower(apellidos) LIKE ?)"
            term = f"%{buscar.lower()}%"
            params.extend([term, term])

        if filtro_esp and filtro_esp != "Todas las Especialidades":
            query += " AND especialidad = ?"
            params.append(filtro_esp)

        if filtro_est and filtro_est != "Todos los Estados":
            query += " AND estado = ?"
            params.append(filtro_est)

        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def actualizar_medico(self, id_medico, nombres, apellidos, especialidad, tel1, tel2, direccion, estado):
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE medicos 
                SET nombres=?, apellidos=?, especialidad=?, telefono1=?, telefono2=?, direccion=?, estado=?
                WHERE id=?
            ''', (nombres, apellidos, especialidad, tel1, tel2, direccion, estado, id_medico))
            conn.commit()
            return True, "Datos actualizados correctamente."
        except sqlite3.Error as e:
            return False, f"Error al actualizar: {e}"
        finally:
            conn.close()

    def eliminar_medico(self, id_medico):
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM medicos WHERE id=?", (id_medico,))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            conn.close()