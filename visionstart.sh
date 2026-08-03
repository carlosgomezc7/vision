#!/usr/bin/env bash
# ==============================================================================
# VISION MCP Server - Script de Lanzamiento Rápido
# CTI Soluciones - Carlos Gómez (Omarch / Arch Linux)
# ==============================================================================

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR" || exit 1

# Detección Automática del Sistema Operativo (Omarch / Arch Linux)
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_NAME="${PRETTY_NAME:-$NAME}"
else
    OS_NAME="$(uname -s)"
fi

echo "🐧 Sistema detectado: $OS_NAME (Kernel $(uname -r))"

VENV_DIR="$PROJECT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "⚠️  Entorno virtual no encontrado en $VENV_DIR. Creando entorno virtual Python..."
    python3 -m venv "$VENV_DIR"
fi

echo "🚀 Activando entorno virtual (.venv)..."
source "$VENV_DIR/bin/activate"

# Verificar si las dependencias requeridas están instaladas
if ! python -c "import fastmcp" 2>/dev/null; then
    echo "📦 Instalando dependencias requeridas desde requirements.txt..."
    pip install -r requirements.txt
fi

echo "✨ Iniciando Servidor FastMCP (VISION)..."
python -m src.main "$@"
