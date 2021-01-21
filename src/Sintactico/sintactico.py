# Analizador sintactico
from Lexico import lexico
import master
from master import Token, Simbolo, Tabla_Simbolos

from Semantico import semantico
from Semantico.semantico import analizar


# ATRIBUTES
global file_lines, sig_token, parse

master.parse = []
master.token_list = []

# FUNCTIONS


def analizador(file_path):
    """o
    Recibe una liena como entrada del analizador general y hace la generacion del arbol
    Manda al analizador semantico el arbol para que este lo analice y anyada atributos
    Pide uno a uno los tokens al analizador lexico
    """
    global file_lines, sig_token

    with open(file_path, 'r') as file:
        file_lines = file.readlines()

    # Obtiene el primer token
    sig_token = pedir_token()
    analizar(0, None, None)  # Se podria meter el nombre del archivo
    # llama al estado inicial
    P()

    tablas = []

    return master.parse, master.token_list, tablas


def pedir_token():
    """
    se encarga de recorrer los elementos del fichero de entrada
    y llamar a la funcion get_token del analizador lexico
    """
    global file_lines, sig_token

    if file_lines:
        master.last_line = True if len(file_lines) == 1 else False

        file_lines[0], token = lexico.get_token(file_lines[0])

        if token == 'null':
            token = pedir_token()

        elif token.key == 'final' and token.value == 'eol':
            file_lines = file_lines[1:]
            master.line_count += 1
            token = pedir_token()

    return token


def error_parse(token):
    # Cambiarlo en funcion de la correccion
    with open(master.file_paths["error"], 'w') as error_file:
        message = 'Error sintactico: '+token.value + \
            ', en linea: '+str(token.linea)+'\n'
        error_file.write(message)
    exit()


# Una función para cada no terminal (y una rama para cada regla)
# Hacer las llamadas al sematico cuando corresponda


def equipara(valor):
    global sig_token

    if 'ID' == valor == sig_token.key:
        sig_token = pedir_token()
    elif 'whole_const' == valor == sig_token.key:
        sig_token = pedir_token()
    elif 'chain' == valor == sig_token.key:
        sig_token = pedir_token()
    elif sig_token.value == valor:
        sig_token = pedir_token()
    else:
        error_parse(Token('equipara', 'error', master.line_count))

    master.token_list.append(sig_token)

# Una función para cada no terminal (y una rama para cada regla)


def E():

    valor = sig_token.value

    if valor == 'not' or valor == 'open_par' or sig_token.key == 'chain' or sig_token.key == 'whole_const' or valor == 'false' or sig_token.key == 'ID' or valor == 'true':
        master.parse.append(1)
        # (not or open_par or chain or whole_const or ...) R E1
        simbolo = R()
        is_boolean = E1(False)
        # Si is_boolean es True, comprobar que R tambien es de tipo boolean y devolver simbolo tipo boolean
        # Si is_boolean es False, devolver simbolo
        analizar(1, simbolo, is_boolean)

    else:
        error_parse(sig_token)

    return simbolo


def E1(is_boolean):
    valor = sig_token.value

    if valor == 'and':
        master.parse.append(2)
        # && R E1
        equipara('and')
        simbolo = R()
        # Comprobar que el simbolo devuelto por R sea de tipo booleano
        # si lo es devolver True en is_boolean
        is_boolean = analizar(2, simbolo, None)
        E1(is_boolean)
    # FOLLOW de E1  =  { ) , ; }
    elif valor == 'close_par' or valor == 'colon' or valor == 'semicolon':
        master.parse.append(3)
    else:
        error_parse(sig_token)

    return simbolo


def R():

    valor = sig_token.value

    if valor == 'not' or valor == 'open_par' or sig_token.key == 'chain' or sig_token.key == 'whole_const' or valor == 'false' or sig_token.key == 'ID' or valor == 'true':
        master.parse.append(4)
        # (not or open_par or ...) U R1
        simbolo = U()
        equals_notequals = R1(False)
        # Similar a como ocurre en U si equals_notequals es false se devuelve el tipo de U
        # si equals_notequals es verdadero se comprueba que U sea booleano y si lo es se devuelve
        simbolo = analizar(4, simbolo, equals_notequals)
    else:
        error_parse(sig_token)

    return simbolo


def R1(equals_notequals):

    valor = sig_token.value

    if valor == 'equals':
        master.parse.append(5)
        # == U R1
        equipara('equals')
        simbolo = U()
        # Comprobar que simbolo sea de tipo numero y si lo es devuelve true
        equals_notequals = analizar(5, simbolo, None)
        R1(equals_notequals)
    elif valor == 'not_equals':
        master.parse.append(6)
        # != U R1
        equipara('not_equals')
        simbolo = U()
        # Comprobar que simbolo sea de tipo numero y si lo es devuelve true
        equals_notequals = analizar(4, simbolo, None)
        simbolo = R1(simbolo)
    elif valor == 'and' or valor == 'close_par' or valor == 'colon' or valor == 'semicolon':
        master.parse.append(7)
    else:
        error_parse(sig_token)

    return simbolo


def U():

    valor = sig_token.value

    if valor == 'not' or valor == 'open_par' or sig_token.key == 'chain' or sig_token.key == 'whole_const' or valor == 'false' or sig_token.key == 'ID' or valor == 'true':
        master.parse.append(8)
        # (not or open_par or ...) V U1
        simbolo = V()
        mas_menos = U1(False)
        # Si mas_menos es True, entonces se comprueba que V sea numero y se devuelve V
        # Si mas_menos es False, entonces se devuelve directamente V
        simbolo = analizar(8, simbolo, mas_menos)
    else:
        error_parse(sig_token)

    return simbolo


def U1(mas_menos):
    # mas_menos es una variable booleana que comprueba si se ha encontrado un mas o un menos en U1

    valor = sig_token.value

    if valor == 'plus':
        master.parse.append(9)
        # + V U1
        equipara('plus')
        simbolo = V()
        # Comprobar que V sea de tipo numero se devuelve true
        mas_menos = analizar(9, simbolo, None)
        U1(mas_menos)
    elif valor == 'minus':
        master.parse.append(10)
        # - V U1
        equipara('minus')
        simbolo = V()
        # Se comprueba que V sea de tipo numero se devuelve tipo true
        mas_menos = analizar(10, simbolo, None)
        U1(mas_menos)
    elif valor == 'not_equals' or valor == 'and' or valor == 'close_par' or valor == 'colon' or valor == 'semicolon' or valor == 'equals':
        master.parse.append(11)
        # sin no entra, mas_menos se mantiene
    else:
        error_parse(sig_token)

    return mas_menos


def V():

    valor = sig_token.value

    if sig_token.key == 'ID':
        master.parse.append(12)
        # ID V1
        token = sig_token
        equipara('ID')
        simbolo = V1()
        # Si 'ID' es una variable se comprueba el tipo del token y devuelve 'ID'.tipo
        # Si 'ID' es una funcion V1 devuelve una lista de los tipos que se le mete
        # al llamar a dicha funcion y devuelve un simbolo de tipo 'function'.dev
        # Si 'ID' es variable, puede que V1 devuelva un simbolo de tipo None en caso de que
        # se tenga que encargar otra etapa de la comprobacion de tipos
        simbolo = analizar(12, simbolo, token)
    elif valor == 'open_par':
        master.parse.append(13)
        # ( E )
        equipara('open_par')
        simbolo = E()
        equipara('close_par')
    elif sig_token.key == 'whole_const':
        master.parse.append(14)
        # whole_const
        equipara('whole_const')
        # Devolvemos simbolo de tipo number
        simbolo = analizar(14, None, None)
    elif sig_token.key == 'chain':
        master.parse.append(15)
        # chain
        equipara('chain')
        # Devolvemos simbolo de tipo chain
        simbolo = analizar(15, None, None)
    elif valor == 'true':
        master.parse.append(16)
        # true
        equipara('true')
        # Devolvemos simbolo de tipo boolean
        simbolo = analizar(16, None, None)
    elif valor == 'false':
        master.parse.append(17)
        # false
        equipara('false')
        # Devolvemos simbolo de tipo boolean
        simbolo = analizar(17, None, None)
    elif valor == 'not':
        master.parse.append(18)
        # not ID
        equipara('not')
        token = sig_token
        equipara('ID')
        # Comprobamos que el 'ID' sea de tipo boolean
        simbolo = analizar(18, None, token)

    return simbolo

# !!!! REALMENTE HACE FALTA UN SIMBOLO DE ENTRADA???
# REVISAR EL SEGUNDO ELIF


def V1():

    valor = sig_token.value

    if valor == 'open_par':
        master.parse.append(19)
        # ( L )
        equipara('open_par')
        # simbolo es la lista de los tipos de variables en L
        simbolo = L()
        equipara('close_par')
    elif valor == 'auto_inc':
        master.parse.append(20)
        # ++
        equipara('auto_inc')
        # el simbolo sera de tipo numero
        simbolo = analizar(20, None, None)
    elif valor == 'not_equals' or valor == 'and' or valor == 'close_par' or valor == 'plus' or valor == 'colon' or valor == 'minus' or valor == 'semicolon' or valor == 'equals':
        master.parse.append(21)
        # revisar su devolucion, puede que sea necesario meter el token
        # hacemos para que devuelva tipo None ya que se comprobara en otro sitio el tipo
        simbolo = analizar(21, None, None)
    else:
        error_parse(sig_token)

    return simbolo


def S():

    valor = sig_token.value

    if sig_token.key == 'ID':
        master.parse.append(22)
        # ID S1
        token = sig_token
        equipara('ID')
        simbolo = S1(simbolo)
        # Si 'ID' es una variable se comprueba el tipo del token y devuelve 'ID'.tipo
        # Si 'ID' es una funcion S1 devuelve una lista de los tipos que se le mete
        # al llamar a dicha funcion y devuelve un simbolo de tipo 'function'.dev
        simbolo = analizar(22, simbolo, token)

    elif valor == 'alert':
        master.parse.append(23)
        # alert ( E ) ;
        equipara('alert')
        equipara('open_par')
        simbolo = E()
        equipara('close_par')
        equipara('semicolon')
        # Se comprueba que el simbolo es de tipo valido para el alert
        analizar(23, simbolo, None)
    elif valor == 'input':
        master.parse.append(24)
        # input ( ID ) ;
        equipara('input')
        equipara('open_par')
        token = sig_token
        equipara('ID')
        equipara('close_par')
        equipara('semicolon')
        # Se comprueba que el simbolo.tipo con nombre 'ID' sea valido como input
        analizar(24, None, token)
    elif valor == 'return':
        master.parse.append(25)
        # return X ;
        equipara('return')
        X()
        equipara('semicolon')
        # comprobamos que el simbolo sea de tipo devolucion de la funcion actual en X()
    else:
        error_parse(sig_token)


def S1(simbolo):

    valor = sig_token.value

    if valor == 'equal':
        master.parse.append(26)
        # = E ;
        equipara('equal')
        simbolo = E()
        equipara('semicolon')
    elif valor == 'open_par':
        master.parse.append(27)
        # ( L ) ;
        equipara('open_par')
        simbolo = L()
        equipara('close_par')
        equipara('semicolon')
    elif valor == 'auto_inc':
        master.parse.append(53)
        # ++ ;
        equipara('auto_inc')
        equipara('semicolon')
        # sematico devuelve tipo numero
        simbolo = analizar(53, None, None)
    else:
        error_parse(sig_token)

    return simbolo


def L():

    valor = sig_token.value
    lista_tipos = []

    if valor == 'not' or valor == 'open_par' or sig_token.key == 'chain' or sig_token.key == 'whole_const' or valor == 'false' or sig_token.key == 'ID' or valor == 'true':
        master.parse.append(28)
        # (not or open_par or ...) E Q
        simbolo = E()
        # Se tiene que implementar en el semantico
        #tipo = simbolo.tipo_dev if simbolo.tipo == 'function' else simbolo.tipo
        tipo = analizar(28, simbolo, None)
        lista_tipos.append(tipo)
        lista_tipos = Q(lista_tipos)
    elif valor == 'close_par':
        master.parse.append(29)
    else:
        error_parse(sig_token)

    return lista_tipos


def Q(lista_tipos):

    valor = sig_token.value

    if valor == 'colon':
        master.parse.append(30)
        # , E Q
        equipara('colon')
        simbolo = E()
        # Se tiene que meter la linea de abajo en el semantico
        #tipo = simbolo.tipo_dev if simbolo.tipo == 'function' else simbolo.tipo
        tipo = analizar(30, simbolo, None)
        lista_tipos.append(tipo)
        lista_tipos = Q(lista_tipos)
    elif valor == 'close_par':
        master.parse.append(31)
    else:
        error_parse(sig_token)

    return lista_tipos


def X():

    valor = sig_token.value

    if valor == 'not' or valor == 'open_par' or sig_token.key == 'chain' or sig_token.key == 'whole_const' or valor == 'false' or sig_token.key == 'ID' or valor == 'true':
        master.parse.append(32)
        # (not or open_par or ...) E
        simbolo = E()
        # Comprobamos que simbolo coincida con el tipo de retorno
        analizar(32, simbolo, None)
    elif valor == 'semicolon':
        master.parse.append(33)
        # Comprobamos que la funcion sea void
        simbolo = analizar(33, None, None)

    else:
        error_parse(sig_token)


def B():

    valor = sig_token.value

    if valor == 'if':
        master.parse.append(34)
        # if ( E ) S
        equipara('if')
        equipara('open_par')
        simbolo = E()
        equipara('close_par')
        S()
        analizar(34, simbolo, None)

    elif valor == 'let':
        master.parse.append(35)
        # let T ID ;
        equipara('let')
        simbolo = T()
        token = sig_token
        equipara('ID')
        equipara('semicolon')
        analizar(35, simbolo, token)

    elif valor == 'alert' or sig_token.key == 'ID' or valor == 'input' or valor == 'return':
        master.parse.append(36)
        # (alert or ID or input or return) S
        token = sig_token
        S()
        analizar(36, simbolo, token)

    elif valor == 'do':
        master.parse.append(37)
        # do { C } while ( E );
        equipara('do')
        equipara('open_braq')
        C()
        equipara('close_braq')
        equipara('while')
        equipara('open_par')
        simbolo = E()
        equipara('close_par')
        equipara('semicolon')
        analizar(37, simbolo, None)
    else:
        error_parse(sig_token)

    return simbolo


def T():

    valor = sig_token.value

    if valor == 'number':
        master.parse.append(38)
        equipara('number')
        simbolo = analizar(38, None, None)
    elif valor == 'boolean':
        master.parse.append(39)
        equipara('boolean')
        simbolo = analizar(39, None, None)
    elif valor == 'string':
        master.parse.append(40)
        equipara('string')
        simbolo = analizar(40, None, None)
    else:
        error_parse(sig_token)

    return simbolo


def F():

    valor = sig_token.value

    if valor == 'function':
        master.parse.append(41)
        # function H ID ( A ) { C }
        equipara('function')
        simbolo = H()
        token = sig_token
        equipara('ID')
        # Crear nueva tabla con nombre del token y tipo del simbolo
        analizar(41, simbolo, token)
        equipara('open_par')
        A()
        equipara('close_par')
        equipara('open_braq')
        C()
        equipara('close_braq')
        # SEMANTICO Y CREAR TABLA DE SIMBOLOS
    else:
        error_parse(sig_token)

    return simbolo


def H():

    valor = sig_token.value

    if valor == 'boolean' or valor == 'number' or valor == 'string':
        master.parse.append(42)
        # (boolean or number or string) T
        simbolo = T()
        # Es una funcion del tipo devuelto por T()
        analizar(42, None, None)
    elif sig_token.key == 'ID':
        master.parse.append(43)
        # Es una funcion void
        analizar(43, None, None)
    else:
        error_parse(sig_token)

    return simbolo


def A():

    valor = sig_token.value

    if valor == 'boolean' or valor == 'number' or valor == 'string':
        master.parse.append(44)
        # (boolean or number or string ) T ID K
        simbolo = T()
        token = sig_token
        equipara('ID')
        # Meter en la funcion el parametro de entrada 'ID' de tipo simbolo
        analizar(44, simbolo, token)
        K()
    elif valor == 'close_par':
        master.parse.append(45)
        # La funcion creada no recibe parametros de entrada
        analizar(45, None, None)
    else:
        error_parse(sig_token)


def K():

    valor = sig_token.value

    if valor == 'colon':
        master.parse.append(46)
        # , T ID K
        equipara('colon')
        simbolo = T()
        token = sig_token
        equipara('ID')
        # Meter en la funcion el parametro de entrada 'ID' de tipo simbolo
        analizar(46, simbolo, token)
        K()
    elif valor == 'close_par':
        master.parse.append(47)
        # Completar la informacion de parametros de entrada en la funcion
        analizar(47, None, None)
    else:
        error_parse(sig_token)


def C():

    valor = sig_token.value

    if valor == 'alert' or valor == 'do' or sig_token.key == 'ID' or valor == 'if' or valor == 'input' or valor == 'let' or valor == 'return':
        master.parse.append(48)
        # ( alert or do or ... ) B C
        B()
        C()
        # Se deberia comprobar que haya return cuando haga falta
        analizar(48, None, None)
    elif valor == 'close_braq':
        master.parse.append(49)
        # Se deberia comprobar que haya return cuando haga falta
        analizar(49, None, None)
    else:
        error_parse(sig_token)


def P():

    valor = sig_token.value

    if valor == 'alert' or valor == 'do' or sig_token.key == 'ID' or valor == 'if' or valor == 'input' or valor == 'let' or valor == 'return':
        master.parse.append(50)
        B()
        P()
    elif valor == 'function':
        master.parse.append(51)
        F()
        P()
    elif valor == '$':
        master.parse.append(52)
        # hemos terminado
        # habra que añadir a TL un dolar al final para saber que hemos acabado el archivo
    else:
        error_parse(sig_token)
