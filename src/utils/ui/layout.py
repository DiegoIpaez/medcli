import os
from .colores import CYAN, BOLD, RESET


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def encabezado(titulo: str, ancho: int = 50):
    print(f"\n  {CYAN}{'=' * ancho}{RESET}")
    print(f"  {BOLD}  {titulo.upper()}{RESET}")
    print(f"  {CYAN}{'=' * ancho}{RESET}\n")


def separador(ancho: int = 50):
    print(f"  {CYAN}{'-' * ancho}{RESET}")
