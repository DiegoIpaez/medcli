from functools import wraps

from ..ui.layout import encabezado, limpiar


def vista(titulo: str):
    """
    Decorador para funciones de tipo "vista" en la CLI.

    Este decorador estandariza el comportamiento visual de las pantallas:
    - Limpia la consola antes de ejecutar la vista.
    - Muestra un encabezado con el título indicado.
    - Luego ejecuta la función original.

    Parameters
    ----------
    titulo : str
        Texto que se mostrará como encabezado de la vista.

    Returns
    -------
    Callable
        Devuelve una función decorada que envuelve a la función original
        agregando comportamiento de layout (limpiar + encabezado).

    Notes
    -----
    - No maneja la pausa (`pausar()`), ya que esa responsabilidad
      queda en la función vista para mayor control del flujo.
    - Utiliza `functools.wraps` para preservar el nombre, docstring
      y metadata de la función original.
    """

    def decorator(func):
        """
        Función que recibe la función original a decorar.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper que ejecuta el layout base antes de llamar
            a la función original.
            """
            limpiar()
            encabezado(titulo)
            return func(*args, **kwargs)

        return wrapper

    return decorator
