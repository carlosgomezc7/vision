## Purpose

Establece las reglas de control de acceso granulares a los recursos de la intranet basadas en principios de Zero Trust y RBAC (Role-Based Access Control).

## Requirements

### Requirement: Evaluación de acceso por defecto
El sistema SHALL denegar el acceso a cualquier recurso de la intranet de forma predeterminada, requiriendo una evaluación explícita de políticas para otorgar acceso.

#### Scenario: Usuario sin permisos intenta acceder
- **WHEN** un usuario autenticado intenta acceder a una URL de un recurso sobre el que no tiene permisos explícitos
- **THEN** el sistema deniega el acceso y devuelve un código de error de autorización (403 Forbidden)

### Requirement: Resolución de políticas combinadas
El sistema SHALL calcular los permisos efectivos de un usuario combinando sus permisos de rol global, permisos de departamento y políticas específicas aplicadas al recurso.

#### Scenario: Usuario con acceso departamental accede a recurso
- **WHEN** un usuario solicita leer un documento y existe una política que permite lectura a su departamento
- **THEN** el sistema evalúa la política y concede el acceso al documento
