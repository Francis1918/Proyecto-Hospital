import re

class HospitalController:
    def __init__(self):
        # Simulación de Base de Datos según el proyecto
        self.pacientes = {"1234567890": {"nombre": "Juan Perez", "hospitalizado": False}}
        self.areas = {"Cuidados Intensivos": 5, "General": 10, "Pediatría": 0}
        self.historiales = {"1234567890": [["2025-01-01", "Gripe", "Alta"]]}

    def validar_cedula(self, cedula):
        if len(cedula) == 10 and cedula.isdigit():
            return True
        return False # Escenario Alternativo 1 [cite: 40]

    def verificar_disponibilidad(self, area):
        return self.areas.get(area, 0) # [cite: 69, 74]

    def registrar_ingreso(self, cedula, motivo, area):
        if not self.validar_cedula(cedula):
            return "Formato de cédula incorrecto"
        if cedula not in self.pacientes:
            return "Paciente no registrado" # [cite: 44]
        if self.pacientes[cedula]["hospitalizado"]:
            return "El paciente ya tiene una hospitalización activa" # [cite: 49]
        if self.verificar_disponibilidad(area) <= 0:
            return "No hay camas disponibles en esta área" # [cite: 70]
        
        self.pacientes[cedula]["hospitalizado"] = True
        self.areas[area] -= 1
        return "Ingreso registrado con éxito" # [cite: 38]

    def registrar_alta(self, cedula, motivo_alta):
        if cedula in self.pacientes and self.pacientes[cedula]["hospitalizado"]:
            self.pacientes[cedula]["hospitalizado"] = False
            return "Alta registrada con éxito" # [cite: 169]
        return "El paciente no tiene una hospitalización activa" # [cite: 180]