import datetime
import subprocess
import sys
from pathlib import Path

from ...ui.colores import BOLD, CYAN, RESET
from ...ui.input import pausar
from ...ui.layout import limpiar
from ...ui.mensajes import exito
from .app_reporte import generar_reporte
from .app_services import (
    obtener_medico_por_turnos_atentidos,
    obtener_medicos,
    obtener_promedio_duracion_por_medico,
    obtener_tasa_ausentismo,
    obtener_turnos_por_mes,
)


def _abrir_pdf(ruta: Path):
    if sys.platform == "win32":
        subprocess.run(["start", str(ruta)], shell=True)
    elif sys.platform == "darwin":
        subprocess.run(["open", str(ruta)])
    else:
        subprocess.run(["xdg-open", str(ruta)])


def _obtener_reports_dir() -> Path:
    """
    Obtiene la ruta root/storage/reports independientemente
    de dónde se ejecute el script.
    """
    root = Path(__file__).resolve().parents[3]
    reports_dir = root / "storage" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir


def generar_reporte_pdf():
    limpiar()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    reports_dir = _obtener_reports_dir()
    ruta = reports_dir / f"{timestamp}_reporte_medcli.pdf"

    generar_reporte(
        str(ruta),
        obtener_tasa_ausentismo(),
        obtener_promedio_duracion_por_medico(),
        obtener_medico_por_turnos_atentidos(),
        obtener_turnos_por_mes(),
        obtener_medicos(),
    )

    exito(f"\n  Reporte generado exitosamente: \n  {ruta}")
    _abrir_pdf(ruta)
    pausar()


def salida():
    limpiar()
    print(f"\n  {CYAN}{'=' * 46}{RESET}")
    print(f"  {BOLD}  Hasta luego!{RESET}")
    print(f"  {CYAN}{'=' * 46}{RESET}\n")
    sys.exit(0)
