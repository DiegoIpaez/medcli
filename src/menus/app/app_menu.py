import sys

from ...ui.colores import BOLD, CYAN, DIM, GREEN, RED, RESET, YELLOW
from ...ui.input import pausar
from ...ui.layout import limpiar
from ..medicos.medicos_menu import menu_medicos
from ..pacientes.pacientes_menu import menu_pacientes

BANNER = r"""
   ____ _     ___ _   _ ___ ____ _
  / ___| |   |_ _| \ | |_ _/ ___/ \
 | |   | |    | ||  \| || | |  / _ \
 | |___| |___ | || |\  || | |_/ ___ \
  \____|_____|___|_| \_|___\___/_/  \_\
"""


def cabecera_principal():
    limpiar()
    separador = "=" * 46
    print(f"{CYAN}{BOLD}{BANNER}{RESET}")
    print(f"  {DIM}  Sistema de Gestion de Turnos Medicos  v1.0.0{RESET}\n")
    print(f"  {CYAN}{separador}{RESET}")
    print(f"  {BOLD}  MENU PRINCIPAL{RESET}")
    print(f"  {CYAN}{separador}{RESET}")
    print(f"  {GREEN}  [1]{RESET}  Gestion de Pacientes")
    print(f"  {GREEN}  [2]{RESET}  Gestion de Medicos")
    print(f"  {GREEN}  [3]{RESET}  Gestion de Turnos")
    print(f"  {GREEN}  [4]{RESET}  Reportes e Informes")
    print(f"  {CYAN}{'-' * 46}{RESET}")
    print(f"  {RED}  [0]{RESET}  Salir")
    print(f"  {CYAN}{separador}{RESET}\n")


def menu_principal():
    while True:
        cabecera_principal()
        opcion = input(f"  {YELLOW}Selecciona una opcion: {RESET}").strip()

        if opcion == "1":
            menu_pacientes()
        elif opcion == "2":
            menu_medicos()
        elif opcion == "3":
            print("No implementado aún.")
        elif opcion == "4":
            print("No implementado aún.")
        elif opcion == "0":
            limpiar()
            print(f"\n  {CYAN}{'=' * 46}{RESET}")
            print(f"  {BOLD}  Hasta luego!{RESET}")
            print(f"  {CYAN}{'=' * 46}{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n  {RED}  Opcion invalida.{RESET}")
            pausar()
