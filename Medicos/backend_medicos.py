import sqlite3

class GestorMedicos:
    def __init__(self, db_name="medicos.db"):
        self.db_name = db_name
        self.inicializar_db()

    def conectar(self):
        """Establece conexión con la base de datos."""
        return sqlite3.connect(self.db_name)

    def inicializar_db(self):
        """Crea la tabla si no existe."""
        conn = self.conectar()
        cursor = conn.cursor()
        
        # CORRECCIÓN: Volvemos a TEXT en teléfonos para conservar el '0' inicial.
        # La validación de que "solo sean números" la hace tu logic_medicos.py
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                especialidad TEXT NOT NULL,
                telefono1 TEXT NOT NULL, 
                telefono2 TEXT,
                direccion TEXT,
                estado TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def registrar_medico(self, nombres, apellidos, especialidad, tel1, tel2, direccion, estado):
        """Inserta un nuevo médico."""
        conn = self.conectar()
        cursor = conn.cursor()
        try:
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
        """
        Obtiene médicos aplicando filtros directamente en SQL.
        """
        conn = self.conectar()
        cursor = conn.cursor()
        
        query = "SELECT * FROM medicos WHERE 1=1"
        params = []

        # Filtro de búsqueda (Nombre o Apellido)
        if buscar:
            query += " AND (lower(nombres) LIKE ? OR lower(apellidos) LIKE ?)"
            term = f"%{buscar.lower()}%"
            params.extend([term, term])

        # Filtro Especialidad
        if filtro_esp and filtro_esp != "Todas las Especialidades":
            query += " AND especialidad = ?"
            params.append(filtro_esp)

        # Filtro Estado (Opcional, preparado para el futuro)
        if filtro_est and filtro_est != "Todos los Estados":
            query += " AND estado = ?"
            params.append(filtro_est)

        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def actualizar_medico(self, id_medico, nombres, apellidos, especialidad, tel1, tel2, direccion, estado):
        """Actualiza un médico existente por su ID."""
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
        """Elimina un médico por su ID."""
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