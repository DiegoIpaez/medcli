from .colores import CYAN, GREEN, RED, RESET, YELLOW


def _mostrar(color, prefijo, texto):
    print(f"\n  {color}{prefijo} {texto}{RESET}")


def exito(texto):
    _mostrar(GREEN, "", texto)


def error(texto):
    _mostrar(RED, "ERR", texto)


def advertencia(texto):
    _mostrar(YELLOW, "!! ", texto)


def info(texto):
    _mostrar(CYAN, ">> ", texto)
