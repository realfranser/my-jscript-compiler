# Analizador semantico
import master
from master import Tabla_Simbolos, Token, Simbolo

tablas = []
tabla_count = 0


def error_semantico(message):
    with open(master.file_paths["error"], 'w') as error_file:
        error_file.write(message + ',linea: ' + str(master.line_count))
    exit()


def analizar(parse, simbolo, token):  # token o simbolo ? ambos

    global tabla_count

    if parse == 0:
        tablas.append(Tabla_Simbolos('0', 'void'))

    elif parse == 2:
        # && U R1  comprovar que es de tipo boolean
        if simbolo.tipo != 'boolean':
            error_semantico(
                'Error Semantico: secuencia tras \'&&\' no es de tipo booleano')
        return Simbolo('and', tipo='boolean')

    elif parse == 5:
        # == U R1  comprovar que es de tipo boolean
        if simbolo.tipo != 'numero':
            error_semantico(
                'Error Semantico: secuencia tras \'==\' no es de tipo booleano')
        return Simbolo('equals', tipo='boolean')

    elif parse == 6:
        # != U R1  comprovar que es de tipo boolean
        if simbolo.tipo != 'numero':
            error_semantico(
                'Error Semantico: secuencia tras \'!=\' no es de tipo booleano')
        return Simbolo('not_equals', tipo='boolean')

    elif parse == 9:
        # + V  comprovar que es de tipo entero
        if simbolo.tipo != 'numero':
            error_semantico(
                'Error Semantico: secuencia tras \'+\' no es de tipo entero')
        return Simbolo('suma', tipo='numero')

    elif parse == 10:
        # - V  comprovar que es de tipo entero
        if simbolo.tipo != 'numero':
            error_semantico(
                'Error Semantico: secuencia tras \'-\' no es de tipo entero')
        return Simbolo('resta', tipo='numero')

    elif parse == 12:
        simbolo_actual = find(Simbolo(token.value))

        if not simbolo_actual:
            tablas[tabla_count].insertar(Simbolo(token.value, tipo='numero'))

        if simbolo_actual.tipo == 'function':
            fun_params = simbolo.tipo_param
            if simbolo_actual.num_param != len(fun_params):

                error_semantico(
                    'num params incorrecto, expected {} have {}'.format(simbolo_actual.num_param, len(fun_params)))
            for p in fun_params:
                print(p.__dict__)
            if not ([param.tipo for param in fun_params] == [param for param in simbolo_actual.tipo_param]):
                error_semantico(
                    'No coinciden los tipos de entrada de la funcion \'{}\''.format(token.value))

            return simbolo_actual

        elif simbolo.lexema == 'autoincremento' and simbolo_actual.tipo != 'numero':
            error_semantico(
                'Error Semantico: Tipo de la variable no coincide con el tipo del valor asignado')

    elif parse == 14:
        # whole_const
        return Simbolo('whole_const', tipo='numero')

    elif parse == 15:
        # chain
        return Simbolo('chain', tipo='string')

    elif parse == 16:
        # true
        return Simbolo('true', tipo='boolean')

    elif parse == 17:
        # false
        return Simbolo('false', tipo='boolean')

    elif parse == 18:
        # not ID
        simbolo_actual = find(Simbolo(token.value))

        if not simbolo_actual:
            error_semantico(
                'Error Semantico: variable sin declarar (se asume de tipo entero), \'{}\' tiene que ser boolean'.format(token.value))

        elif simbolo_actual.tipo != 'boolean':
            error_semantico(
                'Error Semantico: Operacion logica \'not\' aplicada a variable no booleana ')
        return Simbolo('not', tipo='boolean')

    elif parse == 20:
        # ID ++;
        return Simbolo('autoincremento', tipo='numero')

    elif parse == 22:
        # X=3; en caso S
        # problema devuelve simbolo sin tipo
        simbolo_actual = find(Simbolo(token.value))

        if not simbolo_actual:
            tablas[tabla_count].insertar(Simbolo(token.value, tipo='numero'))

        if simbolo_actual.tipo == 'function':
            fun_params = simbolo.tipo_param

            if simbolo_actual.num_param != len(fun_params):
                error_semantico(
                    'num params incorrecto, expected {} have {} '.format(simbolo_actual.num_param, len(fun_params)))

            if not ([param.tipo for param in fun_params] == [param for param in simbolo_actual.tipo_param]):
                error_semantico(
                    'No coinciden los tipos de entrada de la funcion \'{}\''.format(token.value))

            return simbolo_actual

        elif simbolo.tipo == 'function':
            if simbolo.tipo_dev != simbolo_actual.tipo:
                error_semantico(
                    'Error Semantico: Tipo de la variable no coincide con el tipo del valor asignado ')

        elif simbolo_actual.tipo != simbolo.tipo:
            error_semantico(
                'Error Semantico: Tipo de la variable no coincide con el tipo del valor asignado')

    elif parse == 23:
        # alert(E);
        if simbolo.tipo != 'boolean' and simbolo.tipo != 'numero':
            error_semantico(
                'Error Semantico: Argumento en llamada a \'alert()\' no es de tipo boolean o numero')

    elif parse == 24:
        # input(E);
        if simbolo.tipo != 'boolean' and simbolo.tipo != 'numero':
            error_semantico(
                'Error Semantico: Argumento en llamada a \'alert()\' no es de tipo boolean o numero')

    elif parse == 25:
        # return x; // return;
        if not (simbolo.tipo == tablas[tabla_count].retorno or (simbolo.tipo == None and tablas[tabla_count].retorno == 'void')):
            error_semantico(
                'Error Semantico: Tipo return no coincide con el tipo de la funcion')

    elif parse == 34:
        # if(E) X;
        if simbolo.tipo != 'boolean':
            error_semantico(
                'Error Semantico: Clausula evaluada en if() no es de tipo booleano')

    elif parse == 35:
        # let number x;

        # simbolo = nombre 'T', tipo(boolean, numero o string)
        # token = ID

        simbolo = Simbolo(token.value, simbolo.tipo)
        error_semantico('Error Semantico: Variable \'{}\' previamente declarada'.format(token.value)) if tablas[tabla_count].find(
            simbolo) else tablas[tabla_count].insertar(simbolo)

    elif parse == 38:
        return Simbolo('T', tipo='numero')

    elif parse == 39:
        return Simbolo('T', tipo='boolean')

    elif parse == 40:
        return Simbolo('T', tipo='string')

    elif parse == 410:
        # function x(boolean y){let boolean z; return z;}
        error_semantico('Error Semantico: Funcion previamente declarada') if find(
            Simbolo(token.value)) else tablas.append(Tabla_Simbolos(token.value,
                                                                    retorno='void' if simbolo.tipo == 'function' else simbolo.tipo))
        tabla_count = len(tablas) - 1

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

    elif parse == 412:
        tabla_count = 0

    elif parse == 44:
        tablas[tabla_count].insertar(Simbolo(token.value, tipo=simbolo.tipo))

    elif parse == 46:
        tablas[tabla_count].insertar(Simbolo(token.value, tipo=simbolo.tipo))

    elif parse == 53:
        return Simbolo('autoincremento', tipo='numero')


def find(simbolo):

    return tablas[tabla_count].find(simbolo) or tablas[0].find(simbolo)

    # ret = tablas[tabla_count].find(simbolo)

    # if ret != 'null':
    #    return ret
    # ret = tablas[0].find(simbolo)
    # return ret
