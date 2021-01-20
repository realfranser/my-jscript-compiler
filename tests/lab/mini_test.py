

def comprobar(lista):
    if lista:
        print("Algo no ha salido como se esperaba")
    else:
        print("Funciona segun lo esperado")


def sumar_uno(num):
    num += 1
    return num


def cambiar_simbolo(simbolo):
    return simbolo+1


def simbolo_test(simbolo):
    simbolo = cambiar_simbolo(simbolo)
    simbolo = cambiar_simbolo(simbolo)
    return simbolo


def comparador_triple(a, b, c):
    return a == b == c


elem = 'word'


def multiple_triple_comparator(value):
    return ((value and elem) == ('word' or 'pax' or 'cike'))


def except_last(lista):
    for element in lista[:-1]:
        print(element)


class Tipo:

    def __init__(self, lexema):
        self.lexema = lexema


class Lista_tipo:

    def __init__(self, nombre):
        self.nombre = nombre
        self.lista = []

    def find(self, lex):

        #lista = [tipo for tipo in self.lista if tipo.lexema == lex]
        # return lista[0] if lista else None
        return ([tipo for tipo in self.lista if tipo.lexema == lex][:1] or [None])[0]

    def insertar(self, tipo):
        self.lista.append(tipo)


lista_de_tipos = Lista_tipo('prueba')
lista_de_tipos2 = Lista_tipo('prueba2')

for num in range(1, 10):
    lista_de_tipos.insertar(Tipo(str(num)))

for num in range(10, 20):
    lista_de_tipos2.insertar(Tipo(str(num)))


def find(lex):
    #elemento = lista_de_tipos.find(lex)
    # return elemento if elemento else lista_de_tipos2.find(lex)
    return lista_de_tipos.find(lex) or lista_de_tipos2.find(lex)


ts_tipos = ['1', '2', '3']


def comprobar_tipos_28(fun_param):

    if len(ts_tipos) != len(fun_param):
        print('num params incorrecto, expected {} have {}'.format(
            len(ts_tipos), len(fun_param)))

    elif not ([param for param in fun_param] == [param for param in ts_tipos]):
        print('no coinciden los tipos')

    else:
        print('ok')


def main():
    #global lista
    # comprobar(lista)
    # print(sumar_uno(1))
    # print(simbolo_test(1))
    #print(comparador_triple(1, 2, 3))
    #print(comparador_triple(1, 2, 1))
    #print(comparador_triple(1, 1, 1))
    # print(multiple_triple_comparator('pax'))
    # print(multiple_triple_comparator('word'))
    #lista = ['a', 'b', 'c']
    # except_last(lista)
    #lista = [i.lexema for i in lista_tipo]
    # print(lista)
    # print(find('13').lexema)
    # print(find('6').lexema)
    # print(find('50'))  # .lexema)
    comprobar_tipos_28(['1', '2', '3'])
    comprobar_tipos_28(['1', '2'])
    comprobar_tipos_28(['1', '8', '3'])


if __name__ == '__main__':
    main()
