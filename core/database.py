import sqlite3
from sqlite3 import Error

def crear_conexion():
    """Establece la conexión con la base de datos SQLite."""
    try:
        conn = sqlite3.connect('hospital.db')
        # Habilitamos las llaves foráneas para que las relaciones funcionen
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

def inicializar_db():
    """Crea todas las tablas del sistema hospitalario integrado."""
    conn = crear_conexion()
    if conn:
        cursor = conn.cursor()

        # --- NIVEL 1: TABLAS INDEPENDIENTES ---

        # 1. Módulo Pacientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dni TEXT UNIQUE NOT NULL, -- Usado como FK en citas
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT, -- Nombre único según corrección
                email TEXT,
                telefono_referencia TEXT,
                historia_clinica TEXT,
                anamnesis TEXT
            )
        """)

        # 2. Módulo Médicos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                especialidad TEXT NOT NULL,
                telefono1 TEXT,
                telefono2 TEXT,
                direccion TEXT,
                estado TEXT DEFAULT 'Activo'
            )
        """)

        # 3. Módulo Farmacia (Proveedores)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                contacto TEXT,
                telefono TEXT,
                direccion TEXT 
            )
        """)
        
        # 4. Módulo Hospitalización (Salas y Habitaciones)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS salas_habitaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                tipo TEXT NOT NULL,
                estado TEXT DEFAULT 'Disponible'
            )
        """)

        # --- NIVEL 2: TABLAS DEPENDIENTES (Relaciones) ---

        # 5. Inventario (Depende de Proveedores)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                tipo TEXT NOT NULL, -- 'Medicamento' o 'Insumo'
                stock INTEGER DEFAULT 0,
                fecha_caducidad TEXT, -- Obligatorio para el control de vencimientos
                -- Campos específicos de Medicamentos
                presentacion TEXT, 
                requiere_receta INTEGER DEFAULT 0, -- 0=No, 1=Sí
                -- Campos específicos de Insumos
                tipo_material TEXT,
                proveedor_id INTEGER,
                FOREIGN KEY (proveedor_id) REFERENCES proveedores (id)
            )
        """)

        # 6. Modulo Citas (Une Pacientes y Médicos)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,      
                cc_paciente TEXT NOT NULL,        
                id_medico INTEGER NOT NULL, -- Vinculación formal por ID
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                consultorio TEXT,
                estado TEXT DEFAULT 'Confirmada',
                comentario TEXT,
                hora_llegada TEXT, -- Soporte para Módulo 4
                FOREIGN KEY (cc_paciente) REFERENCES pacientes(dni),
                FOREIGN KEY (id_medico) REFERENCES medicos(id)
            )
        """)
        
        # Tabla Notificaciones 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notificaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destinatario TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                canal TEXT DEFAULT 'interno',
                estado TEXT DEFAULT 'Enviada',
                detalle_error TEXT,
                fecha_envio TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 7. Consultas (Alineado con registrar_anamnesis y registrar_diagnostico)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cita_id INTEGER UNIQUE,
                paciente_id INTEGER,
                -- Datos de Triaje (Enfermería)
                peso REAL,
                talla REAL,
                presion_arterial TEXT,
                motivo_consulta TEXT,
                imc REAL,
                -- Datos Médicos (Doctor)
                diagnostico_cie10 TEXT,
                notas_evolucion TEXT,
                fecha_consulta TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cita_id) REFERENCES citas (id),
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
            )
        """)

        # 8. Recetas Médicas (Indispensable para emitir_receta)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consulta_id INTEGER,
                medicamento TEXT NOT NULL, -- Aquí se guarda el campo in_meds
                indicaciones TEXT,
                FOREIGN KEY (consulta_id) REFERENCES consultas (id)
            )
        """)

        # 9. Órdenes de Servicio (Para los <<extend>>: Exámenes, Ecos, etc.)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ordenes_servicio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consulta_id INTEGER,
                tipo_orden TEXT, -- 'Examen', 'Ecografía', 'Tomografía'
                FOREIGN KEY (consulta_id) REFERENCES consultas (id)
            )
        """)        

        # 10. Hospitalización (Depende de Pacientes y Salas)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitalizaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER,
                sala_id INTEGER,
                fecha_ingreso TEXT DEFAULT CURRENT_TIMESTAMP,
                estado_paciente TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
                FOREIGN KEY (sala_id) REFERENCES salas_habitaciones (id)
            )
        """)

        # 11. Entregas Farmacia (Depende de Pacientes y Recetas)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entregas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER,
                receta_id INTEGER,
                fecha_entrega TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
                FOREIGN KEY (receta_id) REFERENCES recetas (id)
            )
        """)
        
        # 12. Pedidos a Proveedores (Depende de Proveedores e Inventario)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos_farmacia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                solicitante TEXT NOT NULL, -- Ej: 'Dr. House'
                diagnostico_referencia TEXT,
                estado TEXT DEFAULT 'Pendiente', -- 'Pendiente', 'Enviado', 'Recibido'
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 13. Tabla detalle para los items del pedido
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedido_detalles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER,
                nombre_item TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos_farmacia (id)
            )
        """)

        conn.commit()
        conn.close()
        print("¡Estructura completa del Hospital creada con éxito!")

if __name__ == '__main__':
    inicializar_db()