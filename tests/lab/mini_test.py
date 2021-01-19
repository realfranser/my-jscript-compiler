

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
    lista = ['a', 'b', 'c']
    except_last(lista)


if __name__ == '__main__':
    main()
