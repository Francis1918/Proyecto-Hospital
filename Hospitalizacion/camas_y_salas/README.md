# Nombres clave para Sala, Habitación y Cama

Este módulo asigna nombres "clave" descriptivos (solo para visualización) sin reemplazar IDs.

Reglas:
- **Sala**: nombre griego por secuencia dentro del mismo piso: Alfa, Beta, Gama, ...
  - Ej.: primera sala en "Planta Baja" → "Alfa"; segunda → "Beta".
- **Habitación**: `<SalaClave> <N>` donde `N` es el índice de la habitación dentro de esa sala.
  - Ej.: "Alfa 1", "Alfa 2".
- **Cama**: `<SalaClave> <N> <Letra>` donde la letra es el orden dentro de la habitación: A, B, C...
  - Ej.: "Alfa 1 A", "Alfa 1 B".

Notas:
- Los nombres clave se muestran en los formularios de registro/consulta y en búsquedas.
- Los IDs (por ejemplo `S-PB-01`, `H-PB-101`, `C-101-1`) siguen siendo los identificadores oficiales.
- La creación de **Habitación** permite seleccionar una **Sala** para definir su relación y nombre.
- La creación de **Cama** pide elegir la **Habitación** destino; el nombre se genera automáticamente.
