# Analizador lexico
import json
import master
from master import line_count, open_comment, Token

# ATRIBUTES


# FUNCTIONS


def generar_error(fallo):
    """
    Le entra de la funcion analizar un error y este devuelve el mensaje de error correspondiente
    """
    with open(master.file_paths["error"], 'w') as error_file:
        message = fallo + '\n'
        error_file.write(message)
    exit()


def generar_token(key, value):
    """
    PUEDE QUE ESTA FUNCION NO HAGA FALTA, SE PUEDE ESCRIBIR EL TOKEN DESDE
    EL SINTACTICO UNA VEZ RECIBIDO
    MODIFICAR EN TOD0 CASO YA QUE LA IMPLEMENTACION ES EXTRANYA
    """
    found = False
    with open(master.file_paths['token_source']) as token_source:
        token_dict = json.load(token_source)
    if key == 'reserved_word':
        for reserved in token_dict["reserved_word"]:
            if reserved == value:
                token = Token(key, value, line_count)
                found = True
                break
        if not found:  # Esto no tiene ningun sentido
            pos = 0  # addToTS(0, value)  # Editar cuando hagamos semantico
            # tabla_simbolos_actual.add(elemento)
            token = Token('ID', str(pos), line_count)
    else:
        token = Token(key, value, line_count)

    return token


def leer_char(lista):
    char = None
    if lista:
        char = lista[0]
    return char


def get_token(lista):
    global open_comment

    contador_caracter = 0
    token = 'null'
    while lista:
        if open_comment == True:  # comentario abierto en otra llamada
            while lista:
                if leer_char(lista) == '*':
                    contador_caracter += 1
                    lista = lista[1:]
                    cerradoEnCaracter = contador_caracter
                    if leer_char(lista) == '/':
                        contador_caracter += 1
                        lista = lista[1:]
                        open_comment = False
                        break
                    else:
                        contador_caracter += 1
                        lista = lista[1:]
                else:
                    contador_caracter += 1
                    lista = lista[1:]
            if(open_comment == False):
                print('!! Atención: */ comentario en bloque cerrado en caracter: ' +
                      str(cerradoEnCaracter)+' ,linea: '+str(line_count))
            if not lista and open_comment and (master.last_line):
                generar_error('++ Error: /* comentario en bloque no se cierra')
                return lista, token

        elif leer_char(lista) == '\n':
            contador_caracter += 1
            lista = lista[1:]
            return lista, Token('final', 'eol', line_count)

        elif leer_char(lista) == ' ' or leer_char(lista) == '\t':
            contador_caracter += 1
            lista = lista[1:]
            lista, token = get_token(lista)

        elif leer_char(lista) == '+':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '+':
                contador_caracter += 1
                lista = lista[1:]
                token = generar_token('auto_inc', 'auto_inc')
            else:
                token = generar_token('arit_op', 'plus')
            return lista, token

        elif leer_char(lista) == '-':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '-':
                contador_caracter += 1
                lista = lista[1:]
                token = generar_token('autoDecOp', 'autodec')
            else:
                token = generar_token('arit_op', 'minus')
            return lista, token

        elif leer_char(lista) == '=':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '=':
                contador_caracter += 1
                lista = lista[1:]
                token = generar_token('rel_op', 'equals')
            else:
                token = generar_token('asig_op', 'equal')
            return lista, token

        elif leer_char(lista) == '!':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '=':
                contador_caracter += 1
                lista = lista[1:]
                token = generar_token('rel_op', 'not_equals')
            else:
                token = generar_token('log_op', 'not')
            return lista, token

        elif leer_char(lista) == '&':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '&':
                contador_caracter += 1
                lista = lista[1:]
                token = generar_token('log_op', 'and')
            else:
                generar_error('++ Error: & esta solo en caracter: ' +
                              str(contador_caracter)+' ,linea: '+str(line_count))
            return lista, token

        elif leer_char(lista) == ',':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'colon')
            return lista, token

        elif leer_char(lista) == ';':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'semicolon')
            return lista, token

        elif leer_char(lista) == '{':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'open_braq')
            return lista, token

        elif leer_char(lista) == '}':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'close_braq')
            return lista, token

        elif leer_char(lista) == '(':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'open_par')
            return lista, token

        elif leer_char(lista) == ')':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'close_par')
            return lista, token

        elif leer_char(lista) == '\'':
            cadena = '\"'
            contador_caracter += 1
            lista = lista[1:]
            seCierra = False
            aperturaEnCaracter = contador_caracter
            while lista:
                cadena = cadena + leer_char(lista)
                if leer_char(lista) == '\'':
                    seCierra = True
                    contador_caracter += 1
                    lista = lista[1:]
                    break
                else:
                    if leer_char(lista) == '\r' or leer_char(lista) == '\n':
                        generar_error('++ Error: \' cadena no se cierra en linea,abierto en caracter: '
                                      + str(aperturaEnCaracter) + ' ,linea: ' + str(line_count))
                        contador_caracter += 1
                        lista = lista[1:]
                        break

                    contador_caracter = contador_caracter + 1
                    lista = lista[1:]

                    if not lista:
                        generar_error('++ Error: \' cadena no se cierra en linea,abierto en caracter: '
                                      + str(aperturaEnCaracter) + ' ,linea: ' + str(line_count))

            if len(cadena) < 67 and seCierra:
                cadena = cadena[:-1]
                cadena = cadena + '\"'
                token = generar_token('chain', cadena)

            elif seCierra:
                generar_error('++ Error: \' cadena supera los 64 caracteres por: '
                              + str(len(cadena)-66) + ' ,en la linea: ' + str(line_count))
            return lista, token

        elif leer_char(lista).isdigit() == True:
            numero = leer_char(lista)
            contador_caracter += 1
            lista = lista[1:]
            while lista:
                if leer_char(lista).isdigit() == True:
                    numero = numero + leer_char(lista)
                    contador_caracter += 1
                    lista = lista[1:]
                else:
                    break

            token = generar_token('whole_const', numero)
            return lista, token

        elif leer_char(lista).isalpha() == True:
            alphanum = leer_char(lista)
            contador_caracter += 1
            lista = lista[1:]
            while lista:
                if leer_char(lista).isalpha() == True or leer_char(lista).isdigit() == True or leer_char(lista) == '_':
                    alphanum = alphanum + leer_char(lista)
                    contador_caracter += 1
                    lista = lista[1:]
                else:
                    break

            token = generar_token('reserved_word', alphanum)
            return lista, token

        elif leer_char(lista) == '/':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '*':
                contador_caracter += 1
                lista = lista[1:]
                open_comment = True
                aperturaEnCaracter = contador_caracter
                while lista:
                    if leer_char(lista) == '*':
                        contador_caracter += 1
                        lista = lista[1:]
                        if leer_char(lista) == '/':
                            contador_caracter += 1
                            lista = lista[1:]
                            open_comment = False
                            break
                        else:
                            contador_caracter += 1
                            lista = lista[1:]
                    else:
                        contador_caracter += 1
                        lista = lista[1:]
                if(open_comment == True):
                    print('!! Atención: /* comentario en bloque no se cierra, abierto en caracter: ' +
                          str(aperturaEnCaracter) + ' ,linea: ' + str(line_count))

            else:
                generar_error('++ Error: / esta solo en caracter: ' +
                              str(contador_caracter)+' ,linea: '+str(line_count))
            return lista, token

        else:
            generar_error('++ Error: Caracter no reconocido:[' + leer_char(
                lista) + '] en caracter: '+str(contador_caracter)+' ,linea: '+str(line_count))
            contador_caracter += 1
            lista = lista[1:]
        lista, token = get_token(lista)

    return lista, token
