import os
from tabulate import tabulate

from .colores import BOLD, CYAN, RESET, RED, GREEN, YELLOW


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def encabezado(titulo: str, ancho: int = 50):
    print(f"\n  {CYAN}{'=' * ancho}{RESET}")
    print(f"  {BOLD}  {titulo.upper()}{RESET}")
    print(f"  {CYAN}{'=' * ancho}{RESET}\n")


def separador(ancho: int = 50):
    print(f"  {CYAN}{'-' * ancho}{RESET}")


def tabla(filas, headers):
    print(tabulate(filas, headers=headers, tablefmt="rounded_outline"))


def menu_opciones(titulo: str, opciones: list, ancho: int = 46) -> str:
    limpiar()
    encabezado(titulo, ancho)

    for clave, emoji, desc in opciones:
        color = RED if clave == "0" else GREEN
        print(f"  {color}  [{clave}]{RESET}  {emoji}  {desc}")

    separador(ancho)
    return input(f"\n  {YELLOW}Selecciona una opcion: {RESET}").strip()
