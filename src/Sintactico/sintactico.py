# Este es el analizador sintactico
from Lexico import lexico


def analizar(linea):
    """
    Recibe una liena como entrada del analizador general y hace la generacion del arbol
    Manda al analizador semantico el arbol para que este lo analice y anyada atributos
    Pide uno a uno los tokens al analizador lexico
    """
    token = lexico.analizar(linea)
    return token
