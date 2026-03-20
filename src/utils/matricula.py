import re


def validar_matricula(matricula):
    """
    Valida el formato de una matrícula médica.

    El formato aceptado es:
    - MN seguido de un espacio y 4 o 6 dígitos (Matrícula Nacional)
    - MP seguido de un espacio y 4 o 6 dígitos (Matrícula Provincial)

    Ejemplos válidos:
        MN 12345
        MN 123456
        MP 54321
        MP 654321

    Args:
        matricula (str): Matrícula médica a validar.

    Returns:
        bool: True si la matrícula tiene un formato válido, False en caso contrario.
    """
    patron = r"^(MN|MP)\s\d{4,6}$"
    return bool(re.match(patron, matricula))
