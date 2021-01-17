# Este es el analizador sintactico
from Lexico import lexico
from Semantico import semantico
import master
from master import Token, Simbolo, Tabla_Simbolos


# ATRIBUTES
global file_lines, char_count


def analizador(file_path):
    """
    Recibe una liena como entrada del analizador general y hace la generacion del arbol
    Manda al analizador semantico el arbol para que este lo analice y anyada atributos
    Pide uno a uno los tokens al analizador lexico
    """
    with open(file_path, 'r') as file:
        file_lines = file.readlines()
        for line in file_lines:
            while line:
                line, token = lexico.get_token(line)
                master.token_list.append(token)


def pedir_token():
    if file_lines[master.line_count]:

    return(lexico.get_token(linea))


def A_sint():
    global sig_token, lineaSint, linea, tokenLines
    linea = leerLinea(tokenLines)
    token = getNextToken()
    sig_token = token.token
    lineaSint = token.linea
    p = P()  # deduzco que es el axioma , en las diapositivas no pone nada
    print(p)
    if sig_token != '$':
        errorParse(Token('A_sint', lineaSint))


def equipara(t):
    global sig_token, lineaSint
    if sig_token == t:
        token = getNextToken()
        sig_token = token.token
        lineaSint = token.linea
    else:
        errorParse(Token('equipara', lineaSint))


def errorParse(error):
    # habra que cambiarlo
    eP = 'ErrorSintactico: Error antes de token \'' + \
        str(error.token) + '\',linea:' + str(error.linea)
    generarError(eP)
    exit()

# Una función para cada no terminal (y una rama para cada regla)


def E():
    print('estoy en e')
    if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true':
        parse.append(1)
        R()
        E1()
    else:
        errorParse(Token(sig_token, lineaSint))


def E1():
    global sig_token
    print('estoy en e1')
    if sig_token == 'and':
        parse.append(2)
        equipara('and')
        r = R()
        e1 = E1()
        if(r.tipo != e1.tipo):  # no se si es asi
            print('error solo para booleanos')
            return Simbolo(0, None, 'err', 0, [], None)

    # FOLLOW de E1  =  { ) , ; }
    elif sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon':
        parse.append(3)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def R():
    print('estoy en r')
    if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true':
        parse.append(4)
        u = U()
        r1 = R1()
        print(u.tipo)
        print(r1.tipo)
        if(u.tipo != r1.tipo):  # no se si es asi
            print('Error en R creo que es de booleano algo asi')
            return Simbolo(0, None, 'err', 0, [], None)

        return Simbolo(0, None, 'boolean', 1, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def R1():
    global sig_token
    print('estoy en r1')
    if sig_token == 'equals':
        parse.append(5)
        equipara('equals')
        u = U()
        r1 = R1()
        if(u.tipo != r1.tipo):  # no se si es asi
            print('Error en R1 no son del msimo tipo')
            return Simbolo(0, None, 'err', 0, [], None)

        return Simbolo(0, None, r1.tipo, r1.despl, [], None)

    elif sig_token == 'notEquals':
        parse.append(6)
        equipara('notEquals')
        u = U()
        r1 = R1()
        if(u.tipo != r1.tipo):  # no se si es asi
            print('Error en R1 no son del msimo tipo')
            return Simbolo(0, None, 'err', 0, [], None)

        return Simbolo(0, None, r1.tipo, r1.despl, [], None)

    elif sig_token == 'and' or sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon':
        parse.append(7)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def U():
    print('estoy en u')
    if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true':
        parse.append(8)
        v = V()
        u1 = U1()
        print(v.tipo)
        print(u1.tipo)
        # if v.tipo != u1.tipo:
        #print('error solo se suman tipos iguales u')
        # return Simbolo(0,None,'err',0,[],None)
        return Simbolo(0, None, v.tipo, v.despl, [], None)

    else:
        errorParse(Token(sig_token, lineaSint))


def U1():
    global sig_token
    print('estoy en u1')
    print(sig_token)
    if sig_token == 'plus':
        parse.append(9)
        equipara('plus')
        v = V()
        u1 = U1()
        if v.tipo != u1.tipo:
            print('error solo se suman tipos iguales u1')
            return Simbolo(0, None, 'err', 0, [], None)
        return Simbolo(0, None, u1.tipo, u1.despl, [], None)
    elif sig_token == 'minus':
        parse.append(10)
        equipara('minus')
        v = V()
        u1 = U1()
        if v.tipo != u1.tipo:
            print('error solo se suman tipos iguales')
            return Simbolo(0, None, 'err', 0, [], None)
        return Simbolo(0, None, u1.tipo, u1.despl, [], None)

    elif sig_token == 'notEquals' or sig_token == 'and' or sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon' or sig_token == 'equals':
        parse.append(11)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def V():
    print('estoy en v')
    print(sig_token)
    if sig_token == 'ID':
        parse.append(12)
        equipara('ID')
        v1 = V1()
        return Simbolo(0, None, 'None', 0, [], None)
    elif sig_token == 'openPar':
        parse.append(13)
        equipara('openPar')
        e = E()
        equipara('closePar')
        return Simbolo(0, None, e.tipo, e.despl, [], None)

    elif sig_token == 'wholeConst':
        parse.append(14)
        equipara('wholeConst')
        return Simbolo(0, None, 'int', 2, [], None)
    elif sig_token == 'chain':
        parse.append(15)
        equipara('chain')
        # no se si esta bien el desp mb = 1
        return Simbolo(0, None, 'chain', 64, [], None)
    elif sig_token == 'true':
        parse.append(16)
        equipara('true')
        return Simbolo(0, None, 'boolean', 1, [], None)
    elif sig_token == 'false':
        parse.append(17)
        equipara('false')
        return Simbolo(0, None, 'boolean', 1, [], None)
    elif sig_token == 'not':
        parse.append(18)
        equipara('not')
        equipara('ID')
        # no se si es asi supongo que es un booleano
        return Simbolo(0, None, 'boolean', 1, [], None)


def V1():
    # print(sig_token)
    if sig_token == 'openPar':
        parse.append(19)
        equipara('openPar')
        l = L()
        equipara('closePar')
        return Simbolo(0, None, 'None', 0, l.param, None)
    elif sig_token == 'autoInc':
        parse.append(20)
        equipara('autoInc')
        # no se si es asi supongo que es un entero
        return Simbolo(0, None, 'int', 2, [], None)
    elif sig_token == 'notEquals' or sig_token == 'and' or sig_token == 'closePar' or sig_token == 'plus' or sig_token == 'colon' or sig_token == 'minus' or sig_token == 'semicolon' or sig_token == 'equals':
        parse.append(21)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def S():
    print('Estoy en s')
    if sig_token == 'ID':
        parse.append(22)
        equipara('ID')
        s1 = S1()
        if(s1.tipo != 'int'):  # revisar va a estar mal
            print('asignado tipo erroneo regla S')
            return Simbolo(0, None, 'err', 0, [], None)

        return Simbolo(0, None, 'ok', 0, [], None)
    elif sig_token == 'alert':
        parse.append(23)
        equipara('alert')
        equipara('openPar')
        e = E()
        equipara('closePar')
        equipara('semicolon')
        return Simbolo(0, None, 'ok', 0, [], None)
    elif sig_token == 'input':
        parse.append(24)
        equipara('input')
        equipara('openPar')
        equipara('ID')
        equipara('closePar')
        equipara('semicolon')
        return Simbolo(0, None, 'ok', 0, [], None)
    elif sig_token == 'return':
        parse.append(25)
        equipara('return')
        x = X()
        equipara('semicolon')
        return Simbolo(0, None, 'ok', x.despl, [], None)


def S1():
    print('estoy en s1')
    if sig_token == 'equal':
        parse.append(26)
        equipara('equal')
        e = E()
        equipara('semicolon')
        return Simbolo(0, None, e.tipo, e.despl, [], None)
    elif sig_token == 'openPar':
        parse.append(27)
        equipara('openPar')
        l = L()
        equipara('closePar')
        equipara('semicolon')
        return Simbolo(0, None, 'None', 0, l.param, None)
    else:
        errorParse(Token(sig_token, lineaSint))


def L():
    # print(sig_token)
    if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true':
        parse.append(28)
        e = E()
        q = Q()
        param = []
        param.append([e.tipo, 0])
        param.append(q.param)
        return Simbolo(0, None, 'None', 0, param, None)
    elif sig_token == 'closePar':
        parse.append(29)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def Q():
    # print(sig_token)
    if sig_token == 'colon':
        parse.append(30)
        equipara('colon')
        e = E()
        q = Q()
        param = []
        param.append([e.tipo, 0])
        param.append(q.param)
    elif sig_token == 'closePar':
        parse.append(31)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def X():
    # print(sig_token)
    if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true':
        parse.append(32)
        e = E()
        return Simbolo(0, None, e.tipo, e.despl, [], None)
    elif sig_token == 'semicolon':
        parse.append(33)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def B():
    print('estoy en b')
    if sig_token == 'if':
        parse.append(34)
        equipara('if')
        equipara('openPar')
        e = E()
        if e.tipo != 'boolean':
            print('error el if solo puede ser boolean')
        equipara('closePar')
        s = S()
        if s.tipo == 'err':
            print('sentencia condicional incorrecta')
        return Simbolo(0, None, s.tipo, 0, [], None)
    elif sig_token == 'let':
        parse.append(35)
        equipara('let')
        t = T()
        equipara('ID')
        equipara('semicolon')
        return Simbolo(0, None, 'None', 0, [], None)  # no se si es asi
    elif sig_token == 'alert' or sig_token == 'ID' or sig_token == 'input' or sig_token == 'return':
        parse.append(36)
        s = S()
        if s.tipo == 'err':
            print('error sentencia incorrecta regla B ')
        return Simbolo(0, None, s.tipo, 0, [], None)
    elif sig_token == 'do':
        parse.append(37)
        equipara('do')
        equipara('openBraq')
        c = C()
        equipara('closeBraq')
        equipara('while')
        equipara('openPar')
        e = E()
        if e.tipo != 'boolean':
            print('error en while , no es un booleano')
        equipara('closePar')
        equipara('semicolon')
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def T():
    # print(sig_token)
    if sig_token == 'number':
        parse.append(38)
        equipara('number')
        return Simbolo(0, None, 'int', 2, [], None)
    elif sig_token == 'boolean':
        parse.append(39)
        equipara('boolean')
        return Simbolo(0, None, 'boolean', 1, [], None)
    elif sig_token == 'string':
        parse.append(40)
        equipara('string')
        return Simbolo(0, None, 'chain', 64, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def F():
    # print(sig_token)
    if sig_token == 'function':
        parse.append(41)
        equipara('function')
        h = H()
        equipara('ID')
        equipara('openPar')
        a = A()
        equipara('closePar')
        equipara('openBraq')
        c = C()
        equipara('closeBraq')
        if(h.tipo == c.tipo):
            return Simbolo(0, None, 'ok', 0, [], None)
        else:
            return Simbolo(0, None, 'err', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def H():
    # print(sig_token)
    if sig_token == 'boolean' or sig_token == 'number' or sig_token == 'string':
        parse.append(42)
        t = T()
        return Simbolo(0, None, t.tipo, t.despl, [], None)
    elif sig_token == 'ID':
        parse.append(43)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def A():
    # print(sig_token)
    if sig_token == 'boolean' or sig_token == 'number' or sig_token == 'string':
        parse.append(44)
        t = T()
        equipara('ID')
        k = K()
        params = []
        params.append([t.tipo, 0])
        for s in k.params:
            params.append([s, 0])
        return Simbolo(0, None, 'None', 0, params, None)
    elif sig_token == 'closePar':
        parse.append(45)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def K():
    # print(sig_token)
    if sig_token == 'colon':
        parse.append(46)
        equipara('colon')
        t = T()
        equipara('ID')
        k = K()
        params = []
        params.append([t.tipo, 0])
        for s in k.params:
            params.append([s, 0])
        return Simbolo(0, None, 'None', 0, params, None)
    elif sig_token == 'closePar':
        parse.append(47)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def C():
    # print(sig_token)
    if sig_token == 'alert' or sig_token == 'do' or sig_token == 'ID' or sig_token == 'if' or sig_token == 'input' or sig_token == 'let' or sig_token == 'return':
        parse.append(48)
        B()
        C()
        return Simbolo(0, None, 'None', 0, [], None)
    elif sig_token == 'closeBraq':
        parse.append(49)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        errorParse(Token(sig_token, lineaSint))


def P():
    # print(sig_token)
    if sig_token == 'alert' or sig_token == 'do' or sig_token == 'ID' or sig_token == 'if' or sig_token == 'input' or sig_token == 'let' or sig_token == 'return':
        parse.append(50)
        B()
        P()
    elif sig_token == 'function':
        parse.append(51)
        F()
        P()
    elif sig_token == '$':
        parse.append(52)
        # hemos terminado
        # habra que añadir a TL un dolar al final para saber que hemos acabado el archivo
    else:
        errorParse(Token(sig_token, lineaSint))
