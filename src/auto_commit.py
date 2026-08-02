"""
auto_commit.py — VISION Auto Commit Tool
Hace un commit automático cada 30 minutos si hay cambios en el repositorio.

Uso:
    python src/auto_commit.py            # corre indefinidamente
    python src/auto_commit.py --once     # ejecuta una sola vez y termina
"""

import subprocess
import time
import argparse
from datetime import datetime

INTERVALO_MINUTOS = 30
INTERVALO_SEGUNDOS = INTERVALO_MINUTOS * 60


def hay_cambios() -> bool:
    """Retorna True si hay archivos modificados o sin seguimiento."""
    resultado = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    return bool(resultado.stdout.strip())


def hacer_commit_y_push() -> None:
    """Agrega todos los cambios, hace commit y push."""
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    mensaje = f"auto: checkpoint {ahora}"

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", mensaje], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"[{ahora}] ✅ Commit y push realizados: '{mensaje}'")


def ciclo() -> None:
    """Verifica cambios y hace commit si los hay."""
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    if hay_cambios():
        print(f"[{ahora}] 🔍 Cambios detectados. Haciendo commit...")
        hacer_commit_y_push()
    else:
        print(f"[{ahora}] ✔ Sin cambios. Nada que commitear.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto commit cada 30 minutos.")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Ejecutar una sola vez y salir.",
    )
    args = parser.parse_args()

    print(f"🚀 VISION Auto Commit iniciado (cada {INTERVALO_MINUTOS} min)")

    if args.once:
        ciclo()
        return

    while True:
        ciclo()
        print(f"   ⏳ Próximo ciclo en {INTERVALO_MINUTOS} minutos...")
        time.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()
