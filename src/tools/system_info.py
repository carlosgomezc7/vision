import platform
import os
import sys

def get_system_info() -> dict:
    """Detecta automáticamente el entorno del sistema operativo (Omarch / Arch Linux)."""
    os_info = {
        "os_name": "Linux",
        "pretty_name": "Arch Linux",
        "kernel": platform.release(),
        "arch": platform.machine(),
        "python_version": sys.version.split()[0],
        "is_arch_based": False,
        "is_omarch": False
    }
    
    os_release_path = "/etc/os-release"
    if os.path.exists(os_release_path):
        with open(os_release_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    val = val.strip('"')
                    if key == "PRETTY_NAME":
                        os_info["pretty_name"] = val
                    elif key == "ID":
                        os_info["id"] = val
    
    if os.path.exists("/etc/arch-release") or os_info.get("id") == "arch":
        os_info["is_arch_based"] = True
    
    hostname = platform.node()
    if "omarch" in hostname.lower() or "omarch" in os_info["pretty_name"].lower():
        os_info["is_omarch"] = True
        
    return os_info

def format_system_info_report() -> str:
    """Devuelve un informe estructurado del sistema operativo detectado."""
    info = get_system_info()
    omarch_tag = " (Omarch / Arch Linux)" if info["is_arch_based"] else ""
    return (
        f"🐧 Sistema Detectado: {info['pretty_name']}{omarch_tag}\n"
        f"🖥️ Kernel: {info['kernel']} ({info['arch']})\n"
        f"🐍 Python: {info['python_version']} (Entorno `.venv`)\n"
        f"📦 Gestor de paquetes base: pacman / yay\n"
        f"⚙️ Estado: Detección automática activa"
    )
