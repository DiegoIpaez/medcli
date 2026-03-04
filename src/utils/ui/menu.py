from .colores import GREEN, RED, RESET, YELLOW
from .layout import encabezado, limpiar, separador


def menu_opciones(titulo: str, opciones: list, ancho: int = 46) -> str:
    limpiar()
    encabezado(titulo, ancho)

    for clave, emoji, desc in opciones:
        color = RED if clave == "0" else GREEN
        print(f"  {color}  [{clave}]{RESET}  {emoji}  {desc}")

    separador(ancho)
    return input(f"\n  {YELLOW}Selecciona una opcion: {RESET}").strip()
