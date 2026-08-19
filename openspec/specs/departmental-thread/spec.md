## Purpose

Representa la comunicación interna segmentada por departamentos, permitiendo hilos de discusión, respuestas y moderación.

## Requirements

### Requirement: Creación de hilos departamentales
El sistema SHALL permitir a los usuarios autorizados de un departamento iniciar un nuevo hilo de discusión.

#### Scenario: Usuario crea un hilo en su departamento
- **WHEN** un usuario autenticado crea un hilo en el foro de su propio departamento
- **THEN** el sistema publica el hilo y permite a otros miembros del departamento visualizarlo y comentarlo

### Requirement: Moderación de hilos
El sistema SHALL permitir a los moderadores del departamento ocultar o archivar hilos que infrinjan políticas.

#### Scenario: Moderador oculta un hilo inapropiado
- **WHEN** un moderador selecciona la acción de ocultar en un hilo de su departamento
- **THEN** el hilo deja de ser visible para los usuarios regulares del departamento
