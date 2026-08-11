# VISION: Servidor de Memoria Sintética y Contexto Empresarial

![Docker Build](https://github.com/carlosgomezc7/vision/actions/workflows/docker-build.yml/badge.svg)

**VISION** es el motor central de **CTI Soluciones**, diseñado como un servidor MCP (Model Context Protocol) para retener el conocimiento estratégico sobre el desarrollo de **Intranets Empresariales B2B con Búsqueda Profunda (Deep Search)**.

## Estructura

| Ruta | Descripción |
|------|-------------|
| `Dockerfile` | Imagen Docker del servidor (método principal de despliegue). |
| `.github/workflows/docker-build.yml` | CI/CD: build y push automático a GHCR en cada push. |
| `src/main.py` | Punto de entrada del servidor FastMCP. |
| `src/memory/` | Almacenamiento SQLite y sembrado de memoria sintética. |
| `src/tools/` | Herramientas especializadas (PRD, UX/WCAG, Issues, Arquitectura). |
| `visionstart.sh` | Script de inicio rápido para desarrollo local con `.venv`. |
| `ISSUES.md` | Registro bilingüe (ES/EN) de incidencias. |

---

## 🚀 Inicio Rápido

### 🐳 Docker (Recomendado)

Construir la imagen localmente:

```bash
docker build -t vision-mcp .
```

O jalar la última imagen desde GitHub Container Registry:

```bash
docker pull ghcr.io/carlosgomezc7/vision:latest
```

Ejecutar el contenedor con volumen persistente para SQLite y ChromaDB:

```bash
docker run -d --name vision -v vision-data:/app/data vision-mcp
```

Ver logs en tiempo real:

```bash
docker logs -f vision
```

Detener y eliminar:

```bash
docker stop vision && docker rm vision
```

### ⚙️ CI/CD (GitHub Actions)

Cada push a `main` ejecuta automáticamente el workflow [docker-build.yml](.github/workflows/docker-build.yml), que:

1. Compila la imagen Docker con Buildx (cache habilitado).
2. La publica en **GitHub Container Registry** (`ghcr.io/carlosgomezc7/vision`).
3. Etiqueta con `latest` y el SHA del commit.

> No necesitas hacer nada extra — cada `git push` actualiza la imagen.

### 🐍 Desarrollo Local (Entorno Virtual)

Si prefieres ejecutar sin Docker, el script configura el `.venv` e instala dependencias automáticamente:

```bash
./visionstart.sh
```

---

## 🛠 Herramientas

### 📌 Registro de Incidencias
El proyecto incluye un registro bilingüe de incidencias en [ISSUES.md](file:///home/carlos/Documents/vision/ISSUES.md) e integración directa con SQLite (`vision_memory.db`).

```bash
python3 -c "from src.tools.issue_tracker import list_recorded_issues; print(list_recorded_issues())"
```

### 🔄 Auto-Commit (Opcional)
Sincroniza cambios a GitHub automáticamente cada 30 minutos:

```bash
python src/auto_commit.py
```
