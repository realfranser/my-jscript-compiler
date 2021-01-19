# Analizador semantico
import master
from master import Tabla_Simbolos, Token

tablas = []
tabla_count = 0


def error_semantico(message):
    with open(master.file_paths["error"], 'w') as error_file:
        error_file.write(message)
    exit()


def analizar(parse, token):

    global tablas, tabla_count
    if parse == 0:
        tablas.append(Tabla_Simbolos('principal'))

    elif parse == 22:
        if not find(token):
            error_semantico(
                'variable no inicializada, en linea: ' + str(token.line))

    elif parse == 12:  # revisar master.arbol
        pass

    elif parse == 1:
        pass
    elif parse == 34:
        if token.tipo != 'boolean':
            error_semantico(
                'if no recibe booleano, en linea: ' + str(token.line))


def find(token):

    return tablas[0].find(token) or tablas[tabla_count].find(token)
