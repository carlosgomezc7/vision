#!/usr/bin/env bash
# ==============================================================================
# VISION MCP Server - Quick Launch Script
# CTI Soluciones - Carlos Gómez (Omarch / Arch Linux)
# ==============================================================================

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR" || exit 1

# Automatic OS detection (Omarch / Arch Linux)
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_NAME="${PRETTY_NAME:-$NAME}"
else
    OS_NAME="$(uname -s)"
fi

echo "🐧 Detected system: $OS_NAME (Kernel $(uname -r))"

VENV_DIR="$PROJECT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "⚠️  Virtual environment not found at $VENV_DIR. Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "🚀 Activating virtual environment (.venv)..."
source "$VENV_DIR/bin/activate"

# Check if required dependencies are installed
if ! python -c "import fastmcp" 2>/dev/null; then
    echo "📦 Installing required dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

echo "✨ Starting FastMCP Server (VISION)..."
python -m src.main "$@"
