# VISION: Servidor de Memoria Sintética y Contexto Empresarial

**VISION** es el motor central de **CTI Soluciones**, diseñado como un servidor MCP (Model Context Protocol) para retener el conocimiento estratégico sobre el desarrollo de **Intranets Empresariales B2B con Búsqueda Profunda (Deep Search)**.

## Estructura
- `visionstart.sh`: Script de inicio rápido del entorno virtual `.venv` y servidor MCP.
- `ISSUES.md`: Registro bilingüe (Español / English) de incidencias e issues.
- `src/main.py`: Punto de entrada del servidor FastMCP.
- `src/memory/`: Almacenamiento SQLite y sembrado de memoria sintética.
- `src/tools/`: Herramientas especializadas (PRD, UX/WCAG, Registro de Issues, Arquitectura).

### 🚀 Inicio Rápido (1 Solo Comando)
Para activar el entorno virtual `.venv` e iniciar el servidor MCP automáticamente, ejecuta desde la raíz:

```bash
./visionstart.sh
```

---

### 📌 Registro de Incidencias e Issues
El proyecto incluye un registro bilingüe de incidencias en [ISSUES.md](file:///home/carlos/Documents/vision/ISSUES.md) e integración directa en la base de datos SQLite (`vision_memory.db`).

- Para consultar o registrar incidencias vía código/MCP:
```bash
python3 -c "from src.tools.issue_tracker import list_recorded_issues; print(list_recorded_issues())"
```

### 🔄 Auto-Commit (Opcional)
En una terminal separada, corre el siguiente script para sincronizar cambios a GitHub automáticamente:

```bash
python src/auto_commit.py
```


