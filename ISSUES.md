# Base de Registro de Incidencias e Issues (VISION - CTI Soluciones)
*Incident & Issue Tracking Log*

Este documento almacena el registro estructurado de incidencias, errores y mejoras del sistema **VISION MCP**, permitiendo seguimiento bilingüe (Español / English).

---

## 📌 Resumen de Incidencias / Issues Summary

| ID | Título / Title | Categoría / Category | Estado / Status | Fecha / Date |
|:--:|:---------------|:---------------------|:---------------:|:------------:|
| **#1** | Activación compleja del entorno virtual (`.venv`) / Virtual environment activation friction | Entorno & Despliegue / Dev Environment | 🟢 Solucionado / Resolved | 2026-08-02 |
| **#2** | Instancias fantasma de Next.js en puerto 3000 / Ghost Next.js dev server port collision | Entorno & Despliegue / Dev Environment | 🟢 Solucionado / Resolved | 2026-08-02 |
| **#3** | Explicación de Variables en Memoria para Nombre de Empresa / Company Name Variable Memory Model | Arquitectura / Architecture | 🟢 Documentado / Documented | 2026-08-02 |

---

## 📋 Detalle de Incidencias / Issue Details

### 🔴 Incidente / Issue #1: Activación compleja del entorno virtual (`.venv`) del MCP

- **ID:** #1
- **Fecha / Date:** 2026-08-02
- **Categoría / Category:** Entorno de Desarrollo / Dev Environment
- **Estado / Status:** 🟢 Solucionado / Resolved
- **Prioridad / Priority:** Media / Medium

#### 🇲🇽 Descripción (Español)
El usuario reportó que resulta complejo o poco práctico iniciar de manera fácil el entorno virtual (`.venv`) del proyecto **VISION MCP** (servidor encagado de apoyar la creación de intranets corporativas y páginas web).

#### 🇺🇸 Description (English)
The user reported difficulty/friction when trying to easily activate the Python virtual environment (`.venv`) for the **VISION MCP** server project.

#### 🛠️ Solución Implementada / Implemented Solution
1. **Script de Lanzamiento Automático (`visionstart.sh`):** Se creó el script ejecutable `./visionstart.sh` en la raíz del proyecto. Este script verifica la existencia de `.venv`, lo activa automáticamente, comprueba las dependencias necesarias y arranca el servidor MCP con un solo comando.
2. **Actualización de Documentación (`README.md`):** Se simplificó la sección de inicio para instruir la ejecución de `./visionstart.sh`.
3. **Base de Datos de Incidencias (`ISSUES.md` y módulo SQLite `src/tools/issue_tracker.py`):** Se implementó un registro persistente para documentar incidencias futuras en español e inglés.
---

### 🔴 Incidente / Issue #2: Instancias fantasma de Next.js en puerto 3000 (Port collision)

- **ID:** #2
- **Fecha / Date:** 2026-08-02
- **Categoría / Category:** Entorno de Desarrollo / Dev Environment
- **Estado / Status:** 🟢 Solucionado / Resolved
- **Prioridad / Priority:** Media / Medium

#### 🇲🇽 Descripción (Español)
Tras actualizar variables y archivos de la aplicación Next.js, los cambios no se reflejaban en el navegador al recargar `http://localhost:3000`. El servidor de desarrollo inició silenciosamente en el puerto `3001` porque había una instancia previa (fantasma) colgada en el puerto `3000`, mostrando una versión desactualizada de la aplicación.

#### 🇺🇸 Description (English)
After updating Next.js variables and config files, changes were not reflecting in the browser at `http://localhost:3000`. The dev server silently started on port `3001` because a previous (ghost) instance was stuck occupying port `3000`, resulting in a cached/stale version of the app being served.

#### 🛠️ Solución Implementada / Implemented Solution
1. **Detección y Limpieza:** Se mató el proceso huérfano utilizando `kill -9 <PID>` que ocupaba el puerto 3000.
2. **Reinicio Limpio:** Se reinició el comando `npm run dev` para forzar que la aplicación arranque en el puerto por defecto, reflejando inmediatamente los cambios en la Landing Page, Login y Dashboard (Ej. actualización a CTI Soluciones).

---

### 🔴 Incidente / Issue #3: Gestión de Memoria y Variables Globales (Nombre de la Empresa)

- **ID:** #3
- **Fecha / Date:** 2026-08-02
- **Categoría / Category:** Arquitectura de Software / Software Architecture
- **Estado / Status:** 🟢 Documentado / Documented
- **Prioridad / Priority:** Informativa / Informational

#### 🇲🇽 Descripción (Español)
El usuario solicitó documentar cómo la aplicación maneja el "estado" o "memoria" para recordar el nombre de la empresa a lo largo de toda la aplicación (desde la Landing Page hasta la sesión privada del Dashboard) tras preguntar "¿Cuál es el nombre del proyecto/empresa?".

#### 🇺🇸 Description (English)
User requested documentation on how the application handles "state" or "memory" to remember the company name throughout the entire application (from the public Landing Page to the private Dashboard session) after answering "What is the name of the project/company?".

#### 🛠️ Solución Implementada / Implemented Solution
Se explicó que la aplicación utiliza dos niveles de memoria:
1. **Memoria Global (Archivo de Configuración):** Se creó un archivo maestro central en `src/lib/config.ts` (objeto `siteConfig`). Cuando definimos el nombre (`Z Soluciones` o `CTI Soluciones`), todas las pantallas (públicas y privadas) consumen esta misma variable. Esto garantiza un comportamiento estático, global y uniforme para todo el portal.
2. **Memoria de Usuario (Base de Datos):** La aplicación está programada (en `dashboard/page.tsx`) con un fallback para leer `user.user_metadata?.company_name` desde Supabase. Si en el futuro el sistema evoluciona a Multi-Tenant (múltiples empresas distintas en el mismo código), el nombre se obtendrá a partir de los datos almacenados de forma persistente y específica para quien inicia sesión.

---
