from .colores import DIM, RESET, WHITE, YELLOW
from .mensajes import error


def pausar(msg="Presiona Enter para continuar..."):
    input(f"\n  {DIM}{msg}{RESET}")


def confirmar(pregunta):
    resp = input(f"\n  {YELLOW}??  {pregunta} [s/N]: {RESET}").strip().lower()
    return resp in ("s", "si", "y", "yes")


def pedir(campo, requerido: bool = True, default=""):
    sufijo = f" [{default}]" if default else (" *" if requerido else " (opcional)")
    while True:
        valor = input(f"  {WHITE}  {campo}{sufijo}: {RESET}").strip()
        if not valor and default:
            return default
        if not valor and requerido:
            error(f"El campo '{campo}' es obligatorio.")
            continue
        return valor
