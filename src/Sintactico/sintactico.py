# Este es el analizador sintactico
from Lexico import lexico
import analizador


def analizar(linea, line_count):
    """
    Recibe una liena como entrada del analizador general y hace la generacion del arbol
    Manda al analizador semantico el arbol para que este lo analice y anyada atributos
    Pide uno a uno los tokens al analizador lexico
    """
    token = lexico.analizar(linea)
    analizador.token_list.append(token)
    analizador.token_file.write('<reserved_word,' + token.atribute + '>\n')
    return token
