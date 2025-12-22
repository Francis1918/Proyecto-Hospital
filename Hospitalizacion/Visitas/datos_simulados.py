# Datos simulados de pacientes
pacientes = [
    {"cedula": "1234567890", "nombre": "Juan Pérez", "estado_clinico": "Estable", "habitacion": "101", "cama": "1", "restricciones": []},
    {"cedula": "0987654321", "nombre": "Ana Gómez", "estado_clinico": "Aislamiento", "habitacion": "102", "cama": "2", "restricciones": []},
    {"cedula": "1122334455", "nombre": "Luis Martínez", "estado_clinico": "Restringido", "habitacion": "103", "cama": "3", "restricciones": []},
]

# Datos simulados de visitantes
visitantes = [
    {"cedula": "5566778899", "nombre": "Carlos López", "apellidos": "García", "restriccion": False},
    {"cedula": "6677889900", "nombre": "María Torres", "apellidos": "Hernández", "restriccion": True},  # Visitante en lista negra
]

# Permisos de visita simulados
permisos_visita = []