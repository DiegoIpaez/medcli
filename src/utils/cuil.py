def validar_cuil(cuil):
    """
    Valida un CUIL argentino verificando formato y dígito verificador.

    El algoritmo multiplica los primeros 10 dígitos por una serie de
    multiplicadores fijos, suma los resultados, y compara el resto
    contra el último dígito del CUIL.

    Ejemplos:
        >>> validar_cuil("20-12345678-9")
        True
        >>> validar_cuil("00-00000000-0")
        False

    Args:
        cuil: CUIL a validar. Acepta guiones y espacios.

    Returns:
        True si el CUIL es válido, False si no.
    """
    MULTIPLICADORES = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    LONGITUD_CUIL = 11
    MODULO = 11
    DIGITO_NULO = 0
    DIGITO_INVALIDO = 10
    DIGITO_REEMPLAZO = 9

    cuil = cuil.replace("-", "").replace(" ", "")

    if len(cuil) != LONGITUD_CUIL or not cuil.isdigit():
        return False

    suma = sum(int(digito) * multiplicador for digito, multiplicador in zip(cuil[:10], MULTIPLICADORES))
    digito_calculado = MODULO - (suma % MODULO)

    if digito_calculado == MODULO:
        digito_calculado = DIGITO_NULO
    if digito_calculado == DIGITO_INVALIDO:
        digito_calculado = DIGITO_REEMPLAZO

    digito_real = int(cuil[-1])
    return digito_calculado == digito_real
