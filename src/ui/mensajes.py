from .colores import CYAN, GREEN, RED, RESET, YELLOW


def _mostrar(color, prefijo, texto):
    pref = f"{prefijo}   " if prefijo else ""
    print(f"\n  {color}{pref}{texto}{RESET}")


def exito(texto, prefijo="✅"):
    _mostrar(GREEN, prefijo, texto)


def error(texto, prefijo="❌"):
    _mostrar(RED, prefijo, texto)


def advertencia(texto, prefijo="⚠️"):
    _mostrar(YELLOW, prefijo, texto)


def info(texto, prefijo="ℹ️"):
    _mostrar(CYAN, prefijo, texto)
