

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


lista_tipo = []

for _ in range(1, 5):
    lista_tipo.append(Tipo('hola'))

for _ in range(1, 5):
    lista_tipo.append(Tipo('adios'))


def devolver_tipo(cond):
    return Tipo('tipo') if cond else None


def main():
    # global lista
    # comprobar(lista)
    # print(sumar_uno(1))
    # print(simbolo_test(1))
    # print(comparador_triple(1, 2, 3))
    # print(comparador_triple(1, 2, 1))
    # print(comparador_triple(1, 1, 1))
    # print(multiple_triple_comparator('pax'))
    # print(multiple_triple_comparator('word'))
    # lista = ['a', 'b', 'c']
    # except_last(lista)
    # lista = [i.lexema for i in lista_tipo]
    # print(lista)
    # print(isinstance([], list))
    # print(['1', '2', '3'] == ['1', '2', '3'])
    # print(['2', '2', '3'] == ['1', '2', '3'])
    # print(['1', '2'] == ['1', '2', '3'])
    print('no coincide') if not devolver_tipo(False) or devolver_tipo(
        False).lexema != 'pax' else print('coincide')

    print('no coincide') if not devolver_tipo(True) or devolver_tipo(
        True).lexema != 'tipo' else print('coincide')


if __name__ == '__main__':
    main()
