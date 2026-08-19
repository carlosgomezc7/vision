## Purpose

Representa comunicados oficiales y anuncios corporativos con control de audiencia, prioridad y confirmación de lectura.

## Requirements

### Requirement: Crear comunicado corporativo
El sistema SHALL permitir a los administradores crear comunicados con título, contenido, autor, departamento, prioridad y audiencia objetivo.

#### Scenario: Administrador publica comunicado
- **WHEN** un usuario con rol de administrador publica un comunicado
- **THEN** el sistema guarda el comunicado y notifica a los usuarios que pertenecen a la audiencia objetivo

### Requirement: Lectura y confirmación
El sistema SHALL registrar qué usuarios han leído un comunicado y permitir solicitar confirmación explícita de lectura.

#### Scenario: Usuario confirma lectura
- **WHEN** un usuario lee un comunicado que requiere confirmación y hace clic en confirmar
- **THEN** el sistema registra la confirmación de lectura con la marca de tiempo correspondiente
