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
    # Se aplican en orden sobre los primeros 10 dígitos del CUIL.
    MULTIPLICADORES = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    LONGITUD_CUIL = 11  # Un CUIL siempre tiene exactamente 11 dígitos sin separadores.
    MODULO = 11  # El algoritmo trabaja en módulo 11.
    DIGITO_NULO = 0  # Si el resultado del módulo es 11, el dígito verificador es 0.
    DIGITO_INVALIDO = 10  # Si el resultado es 10, no existe dígito válido: el CUIL es inválido.

    PREFIJOS_PERSONA_FISICA = {"20", "23", "24", "27"}

    cuil = cuil.replace("-", "").replace(" ", "")

    if len(cuil) != LONGITUD_CUIL or not cuil.isdigit():
        return False

    if cuil[:2] not in PREFIJOS_PERSONA_FISICA:
        return False

    # Cálculo de la suma ponderada: cada uno de los primeros 10 dígitos se multiplica
    # por su multiplicador correspondiente y se suman todos los resultados.
    suma = sum(int(digito) * multiplicador for digito, multiplicador in zip(cuil[:10], MULTIPLICADORES))

    # El dígito verificador esperado es el complemento de la suma en módulo 11.
    digito_calculado = MODULO - (suma % MODULO)

    # Si el resultado es 11, se normaliza a 0 (caso especial del algoritmo).
    if digito_calculado == MODULO:
        digito_calculado = DIGITO_NULO
    if digito_calculado == DIGITO_INVALIDO:
        return False

    # El dígito calculado debe coincidir con el último dígito del CUIL.
    digito_real = int(cuil[-1])
    return digito_calculado == digito_real
