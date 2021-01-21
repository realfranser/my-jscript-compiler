# Analizador semantico
import master
from master import Tabla_Simbolos, Token, Simbolo

tablas = []
tabla_count = 0


def error_semantico(message):
    with open(master.file_paths["error"], 'w') as error_file:
        error_file.write(message)
    exit()


def analizar(parse, simbolo, token):  # token o simbolo ?

    return 1


def find(simbolo):

    return tablas[tabla_count].find(simbolo) or tablas[0].find(simbolo)
