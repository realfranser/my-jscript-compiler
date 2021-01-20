# Analizador lexico
import json
import master
from master import open_comment, Token

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
                token = Token(key, value, master.line_count)
                found = True
                break
        if not found:
            token = Token('ID', value, master.line_count)
    else:
        token = Token(key, value, master.line_count)

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
            if not lista and open_comment and (master.last_line):
                generar_error('++ Error: /* comentario en bloque no se cierra')

        elif master.last_line and lista == '\n':
            token = Token('final', '$', master.line_count)

        elif leer_char(lista) == '\n':
            contador_caracter += 1
            lista = lista[1:]
            token = Token('final', 'eol', master.line_count)

        elif leer_char(lista) == ' ' or leer_char(lista) == '\t':
            contador_caracter += 1
            lista = lista[1:]

        elif leer_char(lista) == '+':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '+':
                contador_caracter += 1
                lista = lista[1:]
                token = generar_token('auto_inc_op', 'auto_inc')
            else:
                token = generar_token('arit_op', 'plus')

        elif leer_char(lista) == '-':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '-':
                contador_caracter += 1
                lista = lista[1:]
                token = generar_token('auto_dec_op', 'auto_dec')
            else:
                token = generar_token('arit_op', 'minus')

        elif leer_char(lista) == '=':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '=':
                contador_caracter += 1
                lista = lista[1:]
                token = generar_token('rel_op', 'equals')
            else:
                token = generar_token('asig_op', 'equal')

        elif leer_char(lista) == '!':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '=':
                contador_caracter += 1
                lista = lista[1:]
                token = generar_token('rel_op', 'not_equals')
            else:
                token = generar_token('log_op', 'not')

        elif leer_char(lista) == '&':
            contador_caracter += 1
            lista = lista[1:]
            if leer_char(lista) == '&':
                contador_caracter += 1
                lista = lista[1:]
                token = generar_token('log_op', 'and')
            else:
                generar_error('++ Error: & esta solo en caracter: ' +
                              str(contador_caracter)+' ,linea: '+str(master.line_count))

        elif leer_char(lista) == ',':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'colon')

        elif leer_char(lista) == ';':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'semicolon')

        elif leer_char(lista) == '{':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'open_braq')

        elif leer_char(lista) == '}':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'close_braq')

        elif leer_char(lista) == '(':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'open_par')

        elif leer_char(lista) == ')':
            contador_caracter += 1
            lista = lista[1:]
            token = generar_token('separator', 'close_par')

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
                                      + str(aperturaEnCaracter) + ' ,linea: ' + str(master.line_count))
                        contador_caracter += 1
                        lista = lista[1:]
                        break

                    contador_caracter = contador_caracter + 1
                    lista = lista[1:]

                    if not lista:
                        generar_error('++ Error: \' cadena no se cierra en linea,abierto en caracter: '
                                      + str(aperturaEnCaracter) + ' ,linea: ' + str(master.line_count))

            if len(cadena) < 67 and seCierra:
                cadena = cadena[:-1]
                cadena = cadena + '\"'
                token = generar_token('chain', cadena)

            elif seCierra:
                generar_error('++ Error: \' cadena supera los 64 caracteres por: '
                              + str(len(cadena)-66) + ' ,en la linea: ' + str(master.line_count))

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

                    elif leer_char(lista) == '\n':
                        return lista, Token('final', 'eol', master.line_count)
                    else:
                        contador_caracter += 1
                        lista = lista[1:]
                if(open_comment == True):
                    print('!! Atención: /* comentario en bloque no se cierra, abierto en caracter: ' +
                          str(aperturaEnCaracter) + ' ,linea: ' + str(master.line_count))

            else:
                generar_error('++ Error: / esta solo en caracter: ' +
                              str(contador_caracter)+' ,linea: '+str(master.line_count))

        else:
            generar_error('++ Error: Caracter no reconocido:[' + leer_char(
                lista) + '] en caracter: '+str(contador_caracter)+' ,linea: '+str(master.line_count))
            contador_caracter += 1
            lista = lista[1:]

        return lista, token

    if (master.last_line and lista == '\n') or (master.last_line and lista == ''):
        token = Token('final', '$', master.line_count)

    return lista, token
