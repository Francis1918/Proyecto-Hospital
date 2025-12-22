# Gestión de Orden Médica

Este módulo gestiona exclusivamente las órdenes médicas asociadas
a pacientes hospitalizados.

## Roles
- Médico: registra y consulta órdenes
- Jefe: consulta órdenes

## Restricciones
- Solo se registran órdenes a pacientes hospitalizados
- No modifica estados clínicos ni infraestructura

## Diseño
El módulo reutiliza la arquitectura del sistema de hospitalización
y el mecanismo de autenticación definido en el UML.
