# Este es el analizador sintactico
from Lexico import lexico
from Semantico import semantico
import master
from master import Token, Simbolo, Tabla_Simbolos, line_count, parse


# ATRIBUTES
global file_lines


# FUNCTIONS
def analizador(file_path):
    """
    Recibe una liena como entrada del analizador general y hace la generacion del arbol
    Manda al analizador semantico el arbol para que este lo analice y anyada atributos
    Pide uno a uno los tokens al analizador lexico
    """
    global file_lines

    with open(file_path, 'r') as file:
        file_lines = file.readlines()

    # llama al estado inicial
    P()


def pedir_token():
    """
    se encarga de recorrer los elementos del fichero de entrada
    y llamar a la funcion get_token del analizador lexico
    """
    global line_count, file_lines

    if file_lines:
        file_lines[0], token = lexico.get_token(file_lines[0])

        if token.key == 'final' and token.entry == 'eol':
            file_lines = file_lines[1:]
            line_count += 1
            token = pedir_token()

        elif token == 'null':
            token = pedir_token()

    return token


def error_parse(token):
    # Cambiarlo en funcion de la correccion
    pass


# Una función para cada no terminal (y una rama para cada regla)
# Hacer las llamadas al sematico cuando corresponda

def E():
    token = pedir_token()
    sig_token = token.value

    if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true':
        parse.append(1)
        R()
        E1()
    else:
        error_parse(token)


def E1():
    token = pedir_token()
    sig_token = token.value

    if sig_token == 'and':
        parse.append(2)
        # equipara('and')
        R()
        E1()

    # FOLLOW de E1  =  { ) , ; }
    elif sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon':
        parse.append(3)
        return Simbolo(0, None, 'None', 0, [], None)
    else:
        error_parse(token)


def R():
    token = pedir_token()
    sig_token = token.value

    if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true':
        parse.append(4)
        U()
        R1()

    else:
        error_parse(token)


def R1():
    token = pedir_token()
    sig_token = token.value

    if sig_token == 'equals':
        parse.append(5)
        U()
        R1()

    elif sig_token == 'notEquals':
        parse.append(6)
        U()
        R1()

    elif sig_token == 'and' or sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon':
        parse.append(7)

    else:
        error_parse(token)


def U():
    token = pedir_token()
    sig_token = token.value

    if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true':
        parse.append(8)
        V()
        U1()

    else:
        error_parse(token)


def U1():
    token = pedir_token()
    sig_token = token.value

    if sig_token == 'plus':
        parse.append(9)
        V()
        U1()

    elif sig_token == 'minus':
        parse.append(10)
        V()
        U1()

    elif sig_token == 'notEquals' or sig_token == 'and' or sig_token == 'closePar' or sig_token == 'colon' or sig_token == 'semicolon' or sig_token == 'equals':
        parse.append(11)

    else:
        error_parse(token)


def V():
    token = pedir_token()
    sig_token = token.value

    if sig_token == 'ID':
        parse.append(12)
        V1()

    elif sig_token == 'openPar':
        parse.append(13)
        E()

    elif sig_token == 'wholeConst':
        parse.append(14)

    elif sig_token == 'chain':
        parse.append(15)

    elif sig_token == 'true':
        parse.append(16)

    elif sig_token == 'false':
        parse.append(17)

    elif sig_token == 'not':
        parse.append(18)

    else:
        error_parse(token)


def V1():
    token = pedir_token()
    sig_token = token.value

    if sig_token == 'openPar':
        parse.append(19)
        L()

    elif sig_token == 'autoInc':
        parse.append(20)

    elif sig_token == 'notEquals' or sig_token == 'and' or sig_token == 'closePar' or sig_token == 'plus' or sig_token == 'colon' or sig_token == 'minus' or sig_token == 'semicolon' or sig_token == 'equals':
        parse.append(21)

    else:
        error_parse(token)


def S():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'ID':
        parse.append(22)
        S1()

    elif sig_token == 'alert':
        parse.append(23)
        E()
    elif sig_token == 'input':
        parse.append(24)
    elif sig_token == 'return':
        parse.append(25)
        X()


def S1():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'equal':
        parse.append(26)
        E()
    elif sig_token == 'openPar':
        parse.append(27)
        L()
    else:
        error_parse(token)


def L():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true':
        parse.append(28)
        E()
        Q()
        param = []
    elif sig_token == 'closePar':
        parse.append(29)
    else:
        error_parse(token)


def Q():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'colon':
        parse.append(30)
        E()
        Q()
    elif sig_token == 'closePar':
        parse.append(31)
    else:
        error_parse(token)


def X():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'not' or sig_token == 'openPar' or sig_token == 'chain' or sig_token == 'wholeConst' or sig_token == 'false' or sig_token == 'ID' or sig_token == 'true':
        parse.append(32)
        E()
    elif sig_token == 'semicolon':
        parse.append(33)
    else:
        error_parse(token)


def B():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'if':
        parse.append(34)
        E()
        S()
    elif sig_token == 'let':
        parse.append(35)
        T()
    elif sig_token == 'alert' or sig_token == 'ID' or sig_token == 'input' or sig_token == 'return':
        parse.append(36)
        S()
    elif sig_token == 'do':
        parse.append(37)
        C()
        E()
    else:
        error_parse(token)


def T():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'number':
        parse.append(38)
    elif sig_token == 'boolean':
        parse.append(39)
    elif sig_token == 'string':
        parse.append(40)
    else:
        error_parse(token)


def F():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'function':
        parse.append(41)
        H()
        A()
        C()
    else:
        error_parse(token)


def H():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'boolean' or sig_token == 'number' or sig_token == 'string':
        parse.append(42)
        T()
    elif sig_token == 'ID':
        parse.append(43)
    else:
        error_parse(token)


def A():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'boolean' or sig_token == 'number' or sig_token == 'string':
        parse.append(44)
        T()
        K()
    elif sig_token == 'closePar':
        parse.append(45)
    else:
        error_parse(token)


def K():
    token = pedir_token()
    sig_token = token.value
    if sig_token == 'colon':
        parse.append(46)
        T()
        K()
    elif sig_token == 'closePar':
        parse.append(47)
    else:
        error_parse(token)


def C():
    token = pedir_token()
    sig_token = token.value

    if sig_token == 'alert' or sig_token == 'do' or sig_token == 'ID' or sig_token == 'if' or sig_token == 'input' or sig_token == 'let' or sig_token == 'return':
        parse.append(48)
        B()
        C()
    elif sig_token == 'closeBraq':
        parse.append(49)
    else:
        error_parse(token)


def P():
    token = pedir_token()
    sig_token = token.value

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
        error_parse(token)
