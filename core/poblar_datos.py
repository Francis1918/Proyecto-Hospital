"""
Script para poblar la base de datos hospital.db con datos de ejemplo.
Utiliza cédulas ecuatorianas válidas según la provincia.
"""
import sqlite3
from datetime import date
from database import crear_conexion

def limpiar_datos_pacientes():
    """Elimina todos los datos existentes en la tabla de pacientes."""
    conn = crear_conexion()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM pacientes")
            conn.commit()
            print("✓ Tabla de pacientes limpiada")
        except Exception as e:
            print(f"✗ Error al limpiar datos: {e}")
        finally:
            conn.close()

def insertar_pacientes_ejemplo():
    """Inserta pacientes de ejemplo con cédulas ecuatorianas válidas."""
    conn = crear_conexion()
    if not conn:
        print("✗ No se pudo conectar a la base de datos")
        return False
    
    cursor = conn.cursor()
    
    # Pacientes de ejemplo con cédulas ecuatorianas válidas
    # Pichincha: inicia con 17
    # Tungurahua: inicia con 18
    pacientes = [
        {
            'dni': '1712345678',  # Pichincha
            'nombres': 'Juan Carlos',
            'apellidos': 'Pérez García',
            'direccion': 'Av. 10 de Agosto N24-253 y Coruña, Quito',
            'telefono': '0991234567',
            'email': 'juan.perez@email.com',
            'telefono_referencia': '0987654321',
            'historia_clinica': '',
            'anamnesis': 'Motivo de consulta: Dolor de cabeza frecuente\nEnfermedad actual: Cefalea tensional de 2 semanas de evolución\nAntecedentes personales: Hipertensión arterial controlada\nAntecedentes familiares: Padre con diabetes tipo 2\nAlergias: Penicilina'
        },
        {
            'dni': '1798765432',  # Pichincha
            'nombres': 'María Elena',
            'apellidos': 'González López',
            'direccion': 'Calle García Moreno S1-47 y Mejía, Quito',
            'telefono': '0998765432',
            'email': 'maria.gonzalez@email.com',
            'telefono_referencia': '0991122334',
            'historia_clinica': '',
            'anamnesis': ''
        },
        {
            'dni': '1803456789',  # Tungurahua
            'nombres': 'Carlos Alberto',
            'apellidos': 'Rodríguez Martínez',
            'direccion': 'Av. Los Guaytambos 03-80, Ambato',
            'telefono': '0976543210',
            'email': 'carlos.rodriguez@email.com',
            'telefono_referencia': '0965432109',
            'historia_clinica': '',
            'anamnesis': ''
        },
    ]
    
    try:
        for paciente in pacientes:
            cursor.execute("""
                INSERT INTO pacientes (
                    dni, nombres, apellidos, direccion, telefono, 
                    email, telefono_referencia, historia_clinica, anamnesis
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                paciente['dni'],
                paciente['nombres'],
                paciente['apellidos'],
                paciente['direccion'],
                paciente['telefono'],
                paciente['email'],
                paciente['telefono_referencia'],
                paciente['historia_clinica'],
                paciente['anamnesis']
            ))
            print(f"✓ Paciente insertado: {paciente['nombres']} {paciente['apellidos']} (CI: {paciente['dni']})")
        
        conn.commit()
        print(f"\n✓ Se insertaron {len(pacientes)} pacientes exitosamente")
        return True
        
    except sqlite3.IntegrityError as e:
        print(f"✗ Error de integridad: {e}")
        print("  (Posiblemente el paciente ya existe)")
        conn.rollback()
        return False
    except Exception as e:
        print(f"✗ Error al insertar pacientes: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def verificar_datos():
    """Verifica que los datos se hayan insertado correctamente."""
    conn = crear_conexion()
    if not conn:
        print("✗ No se pudo conectar a la base de datos")
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT dni, nombres, apellidos FROM pacientes")
    pacientes = cursor.fetchall()
    
    print("\n" + "="*60)
    print("PACIENTES EN LA BASE DE DATOS:")
    print("="*60)
    for dni, nombres, apellidos in pacientes:
        print(f"  • {nombres} {apellidos} - CI: {dni}")
    print("="*60)
    print(f"Total: {len(pacientes)} pacientes\n")
    
    conn.close()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("POBLACIÓN DE BASE DE DATOS - HOSPITAL")
    print("="*60 + "\n")
    
    # Opción para limpiar datos existentes
    respuesta = input("¿Desea limpiar los datos existentes antes de insertar? (s/n): ")
    if respuesta.lower() == 's':
        limpiar_datos_pacientes()
    
    # Insertar datos de ejemplo
    print("\nInsertando pacientes de ejemplo...")
    if insertar_pacientes_ejemplo():
        verificar_datos()
    else:
        print("\n✗ No se pudieron insertar todos los pacientes")
