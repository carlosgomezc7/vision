## Why

Actualmente, el proyecto VISION opera como un conjunto de herramientas aisladas útiles para el desarrollo (generador de PRD, utilidades WCAG, memoria vectorial), pero carece de un modelo de producto unificado guiado por especificaciones claras. Esto crea una brecha masiva entre la visión de negocio (una Intranet B2B robusta) y el código. Necesitamos definir las capacidades fundacionales usando OpenSpec para que actúen como Fuente de Verdad para todo el diseño e implementación técnica futura.

## What Changes

- Inicializar el ecosistema de OpenSpec del proyecto definiendo las capacidades de dominio primarias de la intranet.
- Definir escenarios, requisitos y casos de uso para las comunicaciones corporativas y departamentales.
- Definir los requerimientos para documentos indexables y el sistema de búsqueda profunda (Deep Search).
- Establecer las reglas fundamentales para el control de acceso Zero Trust.

## Capabilities

### New Capabilities
- `corporate-announcement`: Representa comunicados oficiales (título, contenido, autor, prioridad, audiencia, métricas de lectura).
- `departmental-thread`: Representa la comunicación interna por departamentos (moderación, hilos, comentarios).
- `searchable-document`: Representa contenido indexable en el motor de Deep Search con permisos granulares y metadatos.
- `zero-trust-access-policy`: Define las políticas y reglas de control de acceso a los recursos de la intranet por rol/departamento.

### Modified Capabilities
*(Ninguna, no existen capacidades previas modeladas en OpenSpec)*

## Impact

Este cambio es puramente fundacional (arquitectura de información y producto). No modificará inmediatamente la base de código existente en `src/` ni romperá herramientas actuales, pero establecerá el contrato y la fuente de verdad que dictará las futuras implementaciones arquitectónicas y los flujos de las herramientas MCP.
