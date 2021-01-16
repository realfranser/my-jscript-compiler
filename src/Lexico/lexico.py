# Analizador lexico
import json
import master
from master import line_count


def analizar(linea):
    """
    Le manda el sintactico la parte restante de la linea que le falta por analizar
    Cuando el automata finaliza, invoca a generar token
    """
    key = 0
    value = 0
    return generar_token(key, value)


def generar_error(fallo):
    """
    Le entra de la funcion analizar un error y este devuelve el mensaje de error correspondiente
    """
    pass


def generar_token(token_code, atribute):

    found = False
    with open(master.file_paths['token_source']) as token_source:
        token_dict = json.load(token_source)
        if token_code == 'reserved_word':
            for reserved in token_dict['reserved_word']:
                if reserved[atribute] == atribute:
                    token = '<reserved_word,' + atribute + '>\n'
                    tt = Token(atribute, line_count)
                    TL.append(Token(atribute, line_count))
                    found = True
                    break
            if found == False:  # Esto no tiene ningun sentido
                pos = addToTS(0, atribute)  # Editar cuando hagamos semantico
                # el Analizador Lexico añade los lexemas de tipo ID a la Tabla de Símbolos
                token = '<ID,' + str(pos) + '>\n'
                tt = Token('ID', line_count)
                TL.append(Token('ID', line_count))

        else:
            token = '<' + token_code + ',' + atribute + '>\n'
            if(token_code == 'chain' or token_code == 'whole_const'):
                tt = Token(token_code, line_count)
                TL.append(Token(token_code, line_count))
            else:
                tt = Token(atribute, linea)
                TL.append(Token(atribute, line_count))

        tokenFile.write(token)
        sourceTokenFile.close()
        return tt


def generarError(error):
    errorFile.write(error)
    errorFile.write('\n')
    exit()


def leerChar(lista):
    char = None
    if lista:
        char = lista[0]
    return char


def leerlinea(lista):
    linea = None
    if lista:
        linea = lista[0]
    return linea


def get_token(lista):
    global openComment, lastLine
    contadorCaracter = 0
    token = 'null'
    while lista:
       if openComment == True:  # comentario abierto en otra llamada
            while lista:
                if leerChar(lista) == '*':
                    contadorCaracter = contadorCaracter+1
                    lista = lista[1:]
                    cerradoEnCaracter = contadorCaracter
                    if leerChar(lista) == '/':
                        contadorCaracter = contadorCaracter+1
                        lista = lista[1:]
                        openComment = False
                        break
                    else:
                        contadorCaracter = contadorCaracter+1
                        lista = lista[1:]
                else:
                    contadorCaracter = contadorCaracter+1
                    lista = lista[1:]
            if(openComment == False):
                print('!! Atención: */ comentario en bloque cerrado en caracter: ' +
                      str(cerradoEnCaracter)+' ,linea: '+str(lineCounter))
            if not lista and openComment and (lastLine == lineCounter+1):
                generarError('++ Error: /* comentario en bloque no se cierra')
                return lista, token

        elif leerChar(lista) == '\n' or leerChar(lista) == ' ' or leerChar(lista) == '\t':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            print('** Delimitador en caracater:' +
                  str(contadorCaracter)+' ,linea: '+str(lineCounter))

        elif leerChar(lista) == '+':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            if leerChar(lista) == '+':
                contadorCaracter = contadorCaracter+1
                lista = lista[1:]
                token = generar_token('auto_inc', 'auto_inc', lineCounter)
            else:
                token = generar_token('arit_op', 'plus', lineCounter)
            return lista, token

        elif leerChar(lista) == '-':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            if leerChar(lista) == '-':
                contadorCaracter = contadorCaracter+1
                lista = lista[1:]
                token = generar_token('autoDecOp', 'autodec', lineCounter)
            else:
                token = generar_token('arit_op', 'minus', lineCounter)
            return lista, token

        elif leerChar(lista) == '=':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            if leerChar(lista) == '=':
                contadorCaracter = contadorCaracter+1
                lista = lista[1:]
                token = generar_token('rel_op', 'equals', lineCounter)
            else:
                token = generar_token('asig_op', 'equal', lineCounter)
            return lista, token

        elif leerChar(lista) == '!':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            if leerChar(lista) == '=':
                contadorCaracter = contadorCaracter+1
                lista = lista[1:]
                token = generar_token('rel_op', 'notEquals', lineCounter)
            else:
                token = generar_token('log_op', 'not', lineCounter)
            return lista, token

        elif leerChar(lista) == '&':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            if leerChar(lista) == '&':
                contadorCaracter = contadorCaracter+1
                lista = lista[1:]
                token = generar_token('log_op', 'and', lineCounter)
            else:
                generarError('++ Error: & esta solo en caracter: ' +
                             str(contadorCaracter)+' ,linea: '+str(lineCounter))
            return lista, token

        elif leerChar(lista) == ',':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generar_token('separator', 'colon', lineCounter)
            return lista, token

        elif leerChar(lista) == ';':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generar_token('separator', 'semicolon', lineCounter)
            return lista, token

        elif leerChar(lista) == '{':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generar_token('separator', 'open_braq', lineCounter)
            return lista, token

        elif leerChar(lista) == '}':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generar_token('separator', 'close_braq', lineCounter)
            return lista, token

        elif leerChar(lista) == '(':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generar_token('separator', 'open_par', lineCounter)
            return lista, token

        elif leerChar(lista) == ')':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generar_token('separator', 'close_par', lineCounter)
            return lista, token

        elif leerChar(lista) == '\'':
            cadena = '\"'
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            seCierra = False
            aperturaEnCaracter = contadorCaracter
            while lista:
                cadena = cadena + leerChar(lista)
                if leerChar(lista) == '\'':
                    seCierra = True
                    contadorCaracter = contadorCaracter+1
                    lista = lista[1:]
                    break
                else:
                    if leerChar(lista) == '\r' or leerChar(lista) == '\n':
                        generarError('++ Error: \' cadena no se cierra en linea,abierto en caracter: '
                                     + str(aperturaEnCaracter) + ' ,linea: ' + str(lineCounter))
                        contadorCaracter = contadorCaracter+1
                        lista = lista[1:]
                        break

                    contadorCaracter = contadorCaracter + 1
                    lista = lista[1:]

                    if not lista:
                        generarError('++ Error: \' cadena no se cierra en linea,abierto en caracter: '
                                     + str(aperturaEnCaracter) + ' ,linea: ' + str(lineCounter))

            if len(cadena) < 67 and seCierra:
                cadena = cadena[:-1]
                cadena = cadena + '\"'
                token = generar_token('chain', cadena, lineCounter)

            elif seCierra:
                generarError('++ Error: \' cadena supera los 64 caracteres por: '
                             + str(len(cadena)-66) + ' ,en la linea: ' + str(lineCounter))
            return lista, token

        elif leerChar(lista).isdigit() == True:
            numero = leerChar(lista)
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            while lista:
                if leerChar(lista).isdigit() == True:
                    numero = numero + leerChar(lista)
                    contadorCaracter = contadorCaracter+1
                    lista = lista[1:]
                else:
                    break

            token = generar_token('whole_const', numero, lineCounter)
            return lista, token

        elif leerChar(lista).isalpha() == True:
            alphanum = leerChar(lista)
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            while lista:
                if leerChar(lista).isalpha() == True or leerChar(lista).isdigit() == True or leerChar(lista) == '_':
                    alphanum = alphanum + leerChar(lista)
                    contadorCaracter = contadorCaracter+1
                    lista = lista[1:]
                else:
                    break

            token = generar_token('reserved_word', alphanum, lineCounter)
            return lista, token

        elif leerChar(lista) == '/':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            if leerChar(lista) == '*':
                contadorCaracter = contadorCaracter+1
                lista = lista[1:]
                openComment = True
                aperturaEnCaracter = contadorCaracter
                while lista:
                    if leerChar(lista) == '*':
                        contadorCaracter = contadorCaracter+1
                        lista = lista[1:]
                        if leerChar(lista) == '/':
                            contadorCaracter = contadorCaracter+1
                            lista = lista[1:]
                            openComment = False
                            break
                        else:
                            contadorCaracter = contadorCaracter+1
                            lista = lista[1:]
                    else:
                        contadorCaracter = contadorCaracter+1
                        lista = lista[1:]
                if(openComment == True):
                    print('!! Atención: /* comentario en bloque no se cierra, abierto en caracter: ' +
                          str(aperturaEnCaracter) + ' ,linea: ' + str(lineCounter))

            else:
                generarError('++ Error: / esta solo en caracter: ' +
                             str(contadorCaracter)+' ,linea: '+str(lineCounter))
            return lista, token

        else:
            generarError('++ Error: Caracter no reconocido:[' + leerChar(
                lista) + '] en caracter: '+str(contadorCaracter)+' ,linea: '+str(lineCounter))
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
        return lista, token

    return lista, token


