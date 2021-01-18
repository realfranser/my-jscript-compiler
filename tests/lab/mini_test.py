

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


def main():
    #global lista
    # comprobar(lista)
    # print(sumar_uno(1))
    print(simbolo_test(1))


if __name__ == '__main__':
    main()
