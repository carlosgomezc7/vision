"""
auto_commit.py — VISION Auto Commit Tool
Al iniciar pregunta si deseas commits manuales o automáticos cada 30 minutos.

Uso:
    python src/auto_commit.py
"""

import subprocess
import time
from datetime import datetime

INTERVALO_MINUTOS = 30
INTERVALO_SEGUNDOS = INTERVALO_MINUTOS * 60

BANNER = """
╔══════════════════════════════════════════════╗
║       🧠  VISION — Gestor de Commits        ║
╠══════════════════════════════════════════════╣
║  ¿Cómo deseas manejar los commits hoy?      ║
║                                              ║
║  [1] Manual   — Tú decides cuándo commitear ║
║  [2] Auto     — Commit automático c/30 min  ║
╚══════════════════════════════════════════════╝
"""


def hay_cambios() -> bool:
    """Retorna True si hay archivos modificados o sin seguimiento."""
    resultado = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    return bool(resultado.stdout.strip())


def hacer_commit_y_push(mensaje: str | None = None) -> None:
    """Agrega todos los cambios, hace commit y push."""
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    if not mensaje:
        mensaje = f"auto: checkpoint {ahora}"

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", mensaje], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"\n[{ahora}] ✅ Commit y push: '{mensaje}'\n")


def modo_manual() -> None:
    """Modo manual: el usuario decide cuándo commitear."""
    print("\n📝 Modo Manual activado.")
    print("   Comandos disponibles: commit | push | status | salir\n")

    while True:
        try:
            cmd = input("VISION › ").strip().lower()

            if cmd in ("salir", "exit", "q"):
                print("👋 Hasta luego.")
                break

            elif cmd == "status":
                subprocess.run(["git", "status"])

            elif cmd == "commit":
                if not hay_cambios():
                    print("⚠️  No hay cambios para commitear.")
                    continue
                mensaje = input("   Mensaje del commit: ").strip()
                if not mensaje:
                    mensaje = f"manual: cambios {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                hacer_commit_y_push(mensaje)

            elif cmd == "push":
                subprocess.run(["git", "push"], check=True)
                print("✅ Push realizado.")

            else:
                print("   Comandos: commit | push | status | salir")

        except KeyboardInterrupt:
            print("\n👋 Hasta luego.")
            break


def modo_auto() -> None:
    """Modo automático: commit cada 30 minutos."""
    print(f"\n⚙️  Modo Automático activado (cada {INTERVALO_MINUTOS} min).")
    print("   Presiona Ctrl+C para detener.\n")

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
        print("\n⛔ Auto-commit detenido. Hasta luego.")


def elegir_modo() -> str:
    """Muestra el menú y retorna la opción elegida."""
    print(BANNER)
    while True:
        try:
            opcion = input("Selecciona una opción [1/2]: ").strip()
            if opcion in ("1", "2"):
                return opcion
            print("   Por favor ingresa 1 o 2.")
        except KeyboardInterrupt:
            print("\n👋 Saliendo.")
            exit(0)


def main() -> None:
    opcion = elegir_modo()

    if opcion == "1":
        modo_manual()
    elif opcion == "2":
        modo_auto()


if __name__ == "__main__":
    main()
