# Medicos/backend/data_services.py

import csv

class ServicioDatos:
    @staticmethod
    def exportar_csv(archivo_path, datos, columnas):
        """
        Escribe los datos en un archivo CSV.
        :param archivo_path: Ruta del archivo.
        :param datos: Lista de tuplas/listas con los datos de la BD.
        :param columnas: Lista de nombres de columnas para la cabecera.
        :return: (True, "Mensaje") o (False, "Error")
        """
        try:
            # Excluímos la columna 'Acciones' si viene en la lista de columnas UI
            headers = [c for c in columnas if c != "Acciones"]
            
            with open(archivo_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                
                # datos viene como [(id, nombre, ...), ...]
                # Asumimos que la posición 0 es ID y no la queremos en el CSV, 
                # o ajustamos según lo que retorne tu BD.
                # Si tu BD retorna (id, nombre, apellido...), escribimos desde index 1
                for row in datos:
                    writer.writerow(row[1:]) 
            return True, "Datos exportados correctamente."
        except Exception as e:
            return False, f"Error al exportar: {e}"

    @staticmethod
    def importar_csv(archivo_path):
        """
        Lee un CSV y retorna una lista de filas limpias.
        :return: (lista_filas, mensaje_error)
        """
        headers_esperados = ["Nombres", "Apellidos", "Especialidad", "Tel 1", "Tel 2", "Dirección", "Estado"]
        filas_leidas = []
        
        try:
            with open(archivo_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                cabecera = next(reader, None)
                
                # Validación básica de cabecera
                if not cabecera or cabecera != headers_esperados:
                    return None, f"El formato del CSV es incorrecto.\nSe esperaban: {headers_esperados}"
                
                for row in reader:
                    # Filtramos filas vacías
                    if row and len(row) >= 7:
                        filas_leidas.append(row)
                        
            return filas_leidas, None
        except Exception as e:
            return None, f"Error al leer archivo: {e}"