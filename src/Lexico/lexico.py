# Analizador lexico

def analizar(linea):
    """
    Le manda el sintactico la parte restante de la linea que le falta por analizar
    Cuando el automata finaliza, invoca a generar token
    """
    key = 0
    value = 0
    return generar_token(key, value)


def generar_token(key, value):
    """
    Le entra la key y el value del token y lo devuelve
    """
    token = {
        key: value
    }
    return token


def generar_error(fallo):
    """
    Le entra de la funcion analizar un error y este devuelve el mensaje de error correspondiente
    """
    pass
