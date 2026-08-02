"""
auto_commit.py — VISION Auto Commit Tool
Hace un commit y push automático cada 30 minutos si hay cambios.

Uso:
    python src/auto_commit.py
    Ctrl+C para detener.
"""

import subprocess
import time
from datetime import datetime

INTERVALO_MINUTOS = 30
INTERVALO_SEGUNDOS = INTERVALO_MINUTOS * 60


def hay_cambios() -> bool:
    resultado = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    return bool(resultado.stdout.strip())


def hacer_commit_y_push() -> None:
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    mensaje = f"auto: checkpoint {ahora}"
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", mensaje], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"[{ahora}] ✅ Commit y push: '{mensaje}'")


def main() -> None:
    print(f"🚀 VISION Auto Commit activo — ciclo cada {INTERVALO_MINUTOS} min. Ctrl+C para detener.\n")
    try:
        while True:
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
            if hay_cambios():
                print(f"[{ahora}] 🔍 Cambios detectados. Haciendo commit...")
                hacer_commit_y_push()
            else:
                print(f"[{ahora}] ✔ Sin cambios.")
            print(f"   ⏳ Próximo ciclo en {INTERVALO_MINUTOS} minutos...")
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print("\n⛔ Auto-commit detenido.")


if __name__ == "__main__":
    main()
