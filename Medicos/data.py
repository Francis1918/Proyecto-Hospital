import csv
import random

# Nombre del archivo (debe ser el mismo que usa tu programa principal)
ARCHIVO_DB = 'medicos.csv'

# --- DATOS BASE PARA GENERACIÓN ALEATORIA ---
nombres_base = [
    "Juan", "María", "Carlos", "Ana", "Luis", "Elena", "Pedro", "Lucía", "Jorge", "Sofía",
    "Miguel", "Paula", "Andrés", "Valeria", "David", "Camila", "José", "Daniela", "Fernando", "Martina",
    "Ricardo", "Gabriela", "Manuel", "Sara", "Alejandro", "Carmen", "Roberto", "Isabel", "Diego", "Adriana"
]

apellidos_base = [
    "García", "Rodríguez", "López", "Martínez", "González", "Pérez", "Sánchez", "Romero", "Díaz", "Torres",
    "Ruiz", "Vargas", "Castro", "Morales", "Herrera", "Medina", "Aguilar", "Silva", "Mendoza", "Castillo",
    "Ortega", "Rojas", "Guerrero", "Estrada", "Rios", "Vega", "Soto", "Navarro", "Espinoza", "Cevallos"
]

especialidades = ["Medicina General", "Cardiología", "Pediatría", "Dermatología", "Neurología"]
estados = ["Activo", "Inactivo", "Vacaciones", "Licencia"]
calles = ["Av. Amazonas", "Calle Larga", "Av. 6 de Diciembre", "Calle Los Pinos", "Av. Patria", "Calle Sucre", "Av. Eloy Alfaro", "Calle Bolivar"]

def generar_telefono():
    # Genera un número tipo celular 099xxxxxxx
    return f"09{random.randint(10000000, 99999999)}"

def generar_datos_prueba():
    print(f"Generando 100 registros en {ARCHIVO_DB}...")
    
    with open(ARCHIVO_DB, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # HEADER EXACTO que usa tu programa
        writer.writerow(["Nombres", "Apellidos", "Especialidad", "Teléfono 1", "Teléfono 2", "Dirección", "Estado"])
        
        for i in range(100):
            nombre = random.choice(nombres_base)
            apellido = random.choice(apellidos_base)
            especialidad = random.choice(especialidades)
            
            tel1 = generar_telefono()
            # 30% de probabilidad de tener un segundo teléfono
            tel2 = generar_telefono() if random.random() < 0.3 else ""
            
            direccion = f"{random.choice(calles)} N{random.randint(10, 99)}-{random.randint(100, 300)}"
            estado = random.choices(estados, weights=[0.7, 0.1, 0.1, 0.1], k=1)[0] # 70% de probabilidad de estar Activo
            
            writer.writerow([nombre, apellido, especialidad, tel1, tel2, direccion, estado])

    print("¡Listo! Archivo creado exitosamente.")

if __name__ == "__main__":
    generar_datos_prueba()