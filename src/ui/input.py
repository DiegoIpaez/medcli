from .colores import DIM, GREEN, RESET, WHITE, YELLOW
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


def pedir_validado(prompt, validador, msg_error, requerido=True, default=""):
    while True:
        valor = pedir(prompt, requerido=requerido, default=default).strip().upper()
        if validador(valor):
            return valor
        error(msg_error)


def pedir_opcion(prompt, opciones, default=None):
    print()
    for i, op in enumerate(opciones, 1):
        print(f"  {GREEN}  [{i:>2}]{RESET} {op}")

    sufijo = f" [{opciones.index(default) + 1} - {default}]" if default else " *"

    while True:
        entrada = input(f"\n  {YELLOW}  {prompt}{sufijo}: {RESET}").strip()
        if not entrada and default:
            return default
        if entrada.isdigit() and 1 <= int(entrada) <= len(opciones):
            return opciones[int(entrada) - 1]
        error("Opción inválida.")
