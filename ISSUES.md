# Base de Registro de Incidencias e Issues (VISION - CTI Soluciones)
*Incident & Issue Tracking Log*

Este documento almacena el registro estructurado de incidencias, errores y mejoras del sistema **VISION MCP**, permitiendo seguimiento bilingüe (Español / English).

---

## 📌 Resumen de Incidencias / Issues Summary

| ID | Título / Title | Categoría / Category | Estado / Status | Fecha / Date |
|:--:|:---------------|:---------------------|:---------------:|:------------:|
| **#1** | Activación compleja del entorno virtual (`.venv`) / Virtual environment activation friction | Entorno & Despliegue / Dev Environment | 🟢 Solucionado / Resolved | 2026-08-02 |

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
