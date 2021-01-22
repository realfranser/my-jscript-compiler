# Analizador semantico
import master
from master import Tabla_Simbolos, Token, Simbolo

tablas = []
tabla_count = 0


def error_semantico(message):
    with open(master.file_paths["error"], 'w') as error_file:
        error_file.write('Error semantico: ' +
                         message +
                         ', en linea: ' + str(master.line_count))
    exit()


def analizar(parse, simbolo, token):
    global tabla_count

    tabla = tablas[tabla_count] if len(tablas) > 0 else None

    if parse == 0:
        tablas.append(Tabla_Simbolos('0', 'void'))

    elif parse == 1:

        if token and simbolo.tipo != 'boolean':
            error_semantico(
                'un operador logico tine que ir precedido por un valor logico')

    elif parse == 2:

        if simbolo.tipo != 'boolean':
            error_semantico(
                'un operador logico tiene que ir seguido de un valor logico')

        return True

    elif parse == 4:

        if token:
            if simbolo.tipo != 'numero':
                error_semantico(
                    'un comparador tiene que ir precedido por un valor numerico')
            else:
                return Simbolo('R', tipo='boolean')

        else:
            return simbolo

    elif parse == 5:

        if simbolo.tipo != 'numero':
            error_semantico(
                'el operador logico \'==\' tiene que ir seguido de un valor numerico')

        return True

    elif parse == 6:

        if simbolo.tipo != 'numero':
            error_semantico(
                'el operador logico \'!=\' tiene que ir seguido de un valor numerico')

        return True

    elif parse == 8:

        if token and simbolo.tipo != 'numero':
            error_semantico(
                'los operadores numericos tienen que ir precedidos por un valor numerico')

    elif parse == 9:

        if simbolo.tipo != 'numero':
            error_semantico(
                'la suma tiene que ir seguida de un valor numerico')
        else:
            return True

    elif parse == 10:

        if simbolo.tipo != 'numero':
            error_semantico(
                'la resta tiene que ir seguida de un valor numerico')
        else:
            return True

    elif parse == 12:

        entrada = find(token.value)

        if not simbolo:
            return entrada if entrada else Simbolo('V', 'numero')

        if not entrada:
            if simbolo.tipo != 'numero':
                error_semantico(
                    '{} es una variable de tipo y no es compatible con elementos de tipo '.format(token.value))

            tablas[tabla_count].insertar(Simbolo(token.value, tipo='numero'))
            return Simbolo('V', 'numero')

        elif entrada.tipo != 'function':
            if simbolo.tipo != entrada.tipo:
                error_semantico('\'{}\' es una variable de tipo {}'.format(
                    token.value, entrada.tipo if entrada else 'numero'))
            return Simbolo('V', entrada.tipo)

        else:
            if entrada.tipo_param != simbolo.tipo_param:
                error_semantico(
                    'los parametros de entrada en la llamada a la funcion {} no son correctos'.format(token.value))
            return Simbolo('V', entrada.tipo_dev)

    elif parse == 14:

        return Simbolo('V', 'numero')

    elif parse == 15:

        return Simbolo('V', 'string')

    elif parse == 16:

        return Simbolo('V', 'boolean')

    elif parse == 17:

        return Simbolo('V', 'boolean')

    elif parse == 18:

        simbolo = find(token.value)

        if not simbolo or simbolo.tipo != 'boolean':
            error_semantico(
                '{} tiene que ser de tipo boolean para ser operado con \'!\''.format(token.value))

    elif parse == 19:

        return Simbolo('V1', tipo='lista_tipos', tipo_param=simbolo)

    elif parse == 20:

        return Simbolo('V1', 'numero')

    elif parse == 21:

        return None

    elif parse == 22:

        entrada = find(token.value)

        if not entrada:
            if simbolo.tipo != 'numero':
                error_semantico(
                    '{} es una variable de tipo y no es compatible con elementos de tipo '.format(token.value))

            tablas[tabla_count].insertar(Simbolo(token.value, tipo='numero'))

        elif entrada.tipo != 'function':
            if simbolo.tipo != entrada.tipo:
                error_semantico('\'{}\' es una variable de tipo {}'.format(
                    token.value, entrada.tipo if entrada else 'numero'))

        else:
            if entrada.tipo_param != simbolo.tipo_param:
                error_semantico(
                    'los parametros de entrada en la llamada a la funcion {} no son correctos'.format(token.value))

    elif parse == 23:

        if simbolo.tipo != 'numero' and simbolo.tipo != 'string':
            error_semantico('alert solo acepta numeros o strings')

    elif parse == 24:  # si queremos hacerlo con obligacion de declaracion de variables,
        # se puede simplificar

        simbolo = find(token.value)

        if not simbolo:
            tablas[tabla_count].insertar(token.value, tipo='numero')

        tipo = simbolo.tipo if simbolo else 'numero'

        if tipo != 'string' and tipo != 'numero':
            error_semantico('input solo acepta numeros o strings')

    elif parse == 27:

        return Simbolo('S1', tipo='lista_tipos', tipo_param=simbolo)

    elif parse == 53:

        return Simbolo('S1', tipo='numero')

    elif parse == 28:

        return simbolo.tipo_dev if simbolo.tipo == 'function' else simbolo.tipo

    elif parse == 30:

        return simbolo.tipo_dev if simbolo.tipo == 'function' else simbolo.tipo

    elif parse == 32:

        if tabla.retorno != simbolo.tipo:
            error_semantico('la funcion {} devuelve tipos {}, no puede devolver ningun elemento de tipo {}'.format(
                tabla.nombre, tabla.retorno, simbolo.tipo))

    elif parse == 33:

        if tabla.retorno != 'void':
            error_semantico(
                'la funcion {} es de tipo void, no puede devolver ningun elemento'.format(tabla.nombre))

    elif parse == 34:

        if simbolo.tipo != 'boolean':
            error_semantico('la condicion del if no es de tipo boolean')

    elif parse == 35:

        tablas[tabla_count].insertar(Simbolo(token.value, simbolo.tipo)) if not tabla.find(
            token.value) else error_semantico('Se intentando declarar una variable ya declarada')

    elif parse == 37:

        if simbolo.tipo != 'boolean':
            error_semantico(
                'la condicion del while tiene que ser de tipo boolean')

    elif parse == 38:

        return Simbolo('T', 'numero')

    elif parse == 39:

        return Simbolo('T', 'boolean')

    elif parse == 40:

        return Simbolo('T', 'string')

    elif parse == 41:

        tablas.append(Tabla_Simbolos(token.value, simbolo.tipo))
        tabla_count = len(tablas)-1

    elif parse == 42:

        return Simbolo('H', simbolo.tipo)

    elif parse == 43:

        return Simbolo('H', 'void')

    elif parse == 44:

        tablas[tabla_count].insertar(Simbolo(token.value, tipo=simbolo.tipo))

    elif parse == 45:

        tablas[0].insertar(Simbolo(tabla.nombre,
                                   tipo='function',
                                   num_param=0,
                                   tipo_param=None,
                                   tipo_dev=tabla.retorno,
                                   etiqueta=tabla.nombre))

    elif parse == 46:

        tablas[tabla_count].insertar(Simbolo(token.value, tipo=simbolo.tipo))

    elif parse == 47:

        tablas[0].insertar(Simbolo(tabla.nombre,
                                   tipo='function',
                                   num_param=len(tabla.entradas),
                                   tipo_param=[
                                       entry.tipo for entry in tabla.entradas],
                                   tipo_dev=tabla.retorno,
                                   etiqueta=tabla.nombre))

    elif parse == 51:
        tabla_count = 0


def find(id_entrada):

    return tablas[tabla_count].find(id_entrada) or tablas[0].find(id_entrada)
