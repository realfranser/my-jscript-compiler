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

    if parse == 0:
        tablas.append(Tabla_Simbolos('0', 'void'))

    elif parse == 22:
        # X=3;
        simbolo_actual = find(Simbolo(token.value))
        if simbolo_actual == 'null':
            error_semantico('Error Semantico: Variable sin declarar')
        if simbolo_actual.tipo != simbolo.tipo:
            error_semantico(
                'Error Semantico: Tipo de la variable no coincide con el tipo del valor asignado')

    elif parse == 25:

        if not (simbolo.tipo == tablas[tabla_count].retorno or (simbolo.tipo == None and tablas[tabla_count].retorno == 'void')):
            error_semantico(
                'Error Semantico: Tipo return no coincide con el tipo de la funcion')

    elif parse == 34:
        if simbolo.tipo != 'boolean':
            error_semantico(
                'Error Semantico: Clausula evaluada en if() no es de tipo booleano')

    elif parse == 35:
        # let number x;
        simbolo = Simbolo(token.value, simbolo.tipo)
        error_semantico('Error Semantico: Variable \'{}\' previamente declarada'.format(token.value)) if find(
            simbolo) != 'null' else tablas[tabla_count].insertar(simbolo)

    elif parse == 38:
        return Simbolo('T', tipo='numero')

    elif parse == 39:
        return Simbolo('T', tipo='boolean')

    elif parse == 40:
        return Simbolo('T', tipo='string')

    elif parse == 410:
        error_semantico('Error Semantico: Funcion previamente declarada') if find(
            Simbolo(token.value)) != 'null' else tablas.append(Tabla_Simbolos(token.value,
                                                                              retorno='void' if simbolo.tipo == 'function' else simbolo.tipo))
    elif parse == 411:
        # function boolean x(boolean y){let boolean z; return z;}
        tabla = tablas[tabla_count]
        simbolo = Simbolo(lexema=tabla.nombre,
                          tipo='function',
                          num_param=len(tabla.entradas),
                          tipo_param=[
                              entry.tipo for entry in tabla.entradas],
                          tipo_dev=tabla.retorno)

        tablas[0].insertar(simbolo)

    elif parse == 53:
        return Simbolo('autoincremento', tipo='numero')


def find(simbolo):

    ret = tablas[tabla_count].find(simbolo)
    if ret != 'null':
        return simbolo
    ret = tablas[0].find(simbolo)
    return ret
