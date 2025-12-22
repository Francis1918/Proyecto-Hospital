# Gestión de Orden Médica

Este módulo permite el registro y consulta de órdenes médicas
asociadas a pacientes hospitalizados.

## Alcance
- Registrar órdenes médicas
- Consultar órdenes por paciente

## Roles
- MÉDICO: registrar y consultar
- JEFE: consultar

## Restricciones
- Solo se pueden registrar órdenes a pacientes hospitalizados
- El módulo no modifica estados clínicos ni administrativos

## Diseño
Este módulo reutiliza la arquitectura del módulo Gestión de Camas y Salas,
manteniendo separación entre vista, lógica y modelos.
