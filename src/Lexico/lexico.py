# Analizador lexico

def analizar(linea):
    """
    Le manda el sintactico la parte restante de la linea que le falta por analizar
    Cuando el automata finaliza, invoca a generar token
    """
    key = 0
    value = 0
    return generar_token(key, value)


def generar_token(key, value):
    """
    Le entra la key y el value del token y lo devuelve
    """
    token = {
        key: value
    }
    return token


def generar_error(fallo):
    """
    Le entra de la funcion analizar un error y este devuelve el mensaje de error correspondiente
    """
    pass


def generarToken(tokenCode, atribute, linea):

    found = False
    with open(sourceTokenFilePath) as sourceTokenFile:
        data = json.load(sourceTokenFile)
        if tokenCode == 'reservedWord':  # buscar en token.json
            for i in data['tokens']:
                if (i['tokenCode'] == 'reservedWord'):
                    for k in i['tokenList']:
                        if k['atribute'] == atribute:
                            token = '<reservedWord,' + atribute + '>\n'
                            tt = Token(atribute, linea)
                            TL.append(Token(atribute, linea))
                            found = True
                            break
            if found == False:
                pos = addToTS(0, atribute)  # Editar cuando hagamos semantico
                # el Analizador Lexico añade los lexemas de tipo ID a la Tabla de Símbolos
                token = '<ID,' + str(pos) + '>\n'
                tt = Token('ID', linea)
                TL.append(Token('ID', linea))

        else:
            token = '<' + tokenCode + ',' + atribute + '>\n'
            if(tokenCode == 'chain' or tokenCode == 'wholeConst'):
                tt = Token(tokenCode, linea)
                TL.append(Token(tokenCode, linea))
            else:
                tt = Token(atribute, linea)
                TL.append(Token(atribute, linea))

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


def leerLinea(lista):
    linea = None
    if lista:
        linea = lista[0]
    return linea


def analizadorLinea(lista, lineCounter):
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
                token = generarToken('autoIncOp', 'autoinc', lineCounter)
            else:
                token = generarToken('aritOp', 'plus', lineCounter)
            return lista, token

        elif leerChar(lista) == '-':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            if leerChar(lista) == '-':
                contadorCaracter = contadorCaracter+1
                lista = lista[1:]
                token = generarToken('autoDecOp', 'autodec', lineCounter)
            else:
                token = generarToken('aritOp', 'minus', lineCounter)
            return lista, token

        elif leerChar(lista) == '=':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            if leerChar(lista) == '=':
                contadorCaracter = contadorCaracter+1
                lista = lista[1:]
                token = generarToken('relOp', 'equals', lineCounter)
            else:
                token = generarToken('asigOp', 'equal', lineCounter)
            return lista, token

        elif leerChar(lista) == '!':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            if leerChar(lista) == '=':
                contadorCaracter = contadorCaracter+1
                lista = lista[1:]
                token = generarToken('relOp', 'notEquals', lineCounter)
            else:
                token = generarToken('logOp', 'not', lineCounter)
            return lista, token

        elif leerChar(lista) == '&':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            if leerChar(lista) == '&':
                contadorCaracter = contadorCaracter+1
                lista = lista[1:]
                token = generarToken('logOp', 'and', lineCounter)
            else:
                generarError('++ Error: & esta solo en caracter: ' +
                             str(contadorCaracter)+' ,linea: '+str(lineCounter))
            return lista, token

        elif leerChar(lista) == ',':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generarToken('separator', 'colon', lineCounter)
            return lista, token

        elif leerChar(lista) == ';':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generarToken('separator', 'semicolon', lineCounter)
            return lista, token

        elif leerChar(lista) == '{':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generarToken('separator', 'openBraq', lineCounter)
            return lista, token

        elif leerChar(lista) == '}':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generarToken('separator', 'closeBraq', lineCounter)
            return lista, token

        elif leerChar(lista) == '(':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generarToken('separator', 'openPar', lineCounter)
            return lista, token

        elif leerChar(lista) == ')':
            contadorCaracter = contadorCaracter+1
            lista = lista[1:]
            token = generarToken('separator', 'closePar', lineCounter)
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
                token = generarToken('chain', cadena, lineCounter)

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

            token = generarToken('wholeConst', numero, lineCounter)
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

            token = generarToken('reservedWord', alphanum, lineCounter)
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
