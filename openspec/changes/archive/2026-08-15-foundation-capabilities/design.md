## Context

Actualmente el servidor MCP de VISION está compuesto por herramientas técnicas (WCAG, W3C Tokens, System Info) que asisten en el desarrollo pero no operan sobre un modelo de dominio vivo de la intranet. Este cambio sienta las bases (Ver `proposal.md`) para migrar hacia un ecosistema guiado por especificaciones donde OpenSpec sea la verdadera fuente de la verdad para el comportamiento del producto.

## Goals / Non-Goals

**Goals:**
- Establecer un esquema formal y verificable para las 4 capacidades core de la Intranet.
- Proveer un contrato claro (Behavioral Contract) para futuras implementaciones de backend, frontend y motores de búsqueda.

**Non-Goals:**
- No se implementará código de base de datos ni esquemas SQL/Supabase en esta fase.
- No se modificarán las herramientas MCP existentes para leer estos specs todavía; esta fase es puramente de modelado de dominio.

## Decisions

### 1. OpenSpec como "Single Source of Truth" para Dominio
Se decide que todo comportamiento funcional de la Intranet (Ej. confirmación de lectura, políticas Zero Trust) debe existir primero como un requisito formal (`SHALL`) y un escenario evaluable (`WHEN/THEN`) en OpenSpec antes de escribirse código.
*Alternativa considerada*: Usar directamente diagramas UML o schemas de base de datos. Se descartó porque no capturan el comportamiento observable del usuario y son demasiado acoplados a la implementación tecnológica.

### 2. Diseño Agnóstico a la Tecnología
Las especificaciones se han redactado sin referenciar explícitamente bases de datos específicas (SQLite, PostgreSQL, Supabase) ni frameworks de frontend (React, Vue).
*Razón*: Permite a VISION tomar decisiones de arquitectura (AWS vs On-Premise, etc.) en fases posteriores (ADR) sin invalidar las reglas de negocio.

## Risks / Trade-offs

- **[Riesgo] Desalineación entre Specs y Código futuro**: Que los desarrolladores escriban código que ignore estas especificaciones.
  - **Mitigación**: El agente VISION utilizará los archivos en `openspec/specs/` como contexto obligatorio antes de generar PRDs o revisar Pull Requests en el futuro.
