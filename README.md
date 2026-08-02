# VISION: Servidor de Memoria Sintética y Contexto Empresarial

**VISION** es el motor central de **CTI Soluciones**, diseñado como un servidor MCP (Model Context Protocol) para retener el conocimiento estratégico sobre el desarrollo de **Intranets Empresariales B2B con Búsqueda Profunda (Deep Search)**.

## Estructura
- `src/main.py`: Punto de entrada del servidor FastMCP.
- `src/memory/`: Almacenamiento vectorial y sembrado de memoria.
- `src/tools/`: Herramientas especializadas para PRDs, Arquitectura y Retrospectivas.
- `src/seed_data/`: Documentación base de conocimiento.

### Comando rápido
```bash
source .venv/bin/activate && python -m src.main
```

### 0. Activar auto-commit (commits automáticos cada 30 min)
En una terminal separada, corre el siguiente script para que los cambios se suban a GitHub automáticamente:

```bash
python src/auto_commit.py
```

> Detecta cambios en el repositorio y hace `git add`, `commit` y `push` cada 26 minutos. Usa `Ctrl+C` para detenerlo.


### 1. Activar el entorno virtual
```bash
source .venv/bin/activate
```

### 2. Instalar dependencias (solo la primera vez)
```bash
pip install -r requirements.txt
```

### 3. Iniciar el servidor MCP
```bash
python -m src.main
```

